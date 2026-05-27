from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from pathlib import PurePosixPath
from uuid import UUID

from fastapi import HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.db.models import BlogPost, BlogProtectedDocument, BlogProtectedDocumentGroup, MediaFile
from app.domains.media.service.resolver import sanitize_public_download_filename
from app.domains.media.service.storage import AdminMediaStorageService
from app.domains.public_site.schema.blog import ProtectedDocumentGroupOut, ProtectedDocumentOut
from app.services.request_protection import _extract_request_ip, enforce_rate_limit_or_429
from app.services.security import verify_password


def _localized_text(default_value: str | None, localized_value: str | None, locale: str) -> str | None:
    if locale != 'en' and localized_value:
        return localized_value
    return default_value


def list_protected_document_groups_for_blog(session: Session, *, blog_slug: str, locale: str) -> list[ProtectedDocumentGroupOut]:
    groups = session.scalars(
        select(BlogProtectedDocumentGroup)
        .join(BlogPost, BlogPost.id == BlogProtectedDocumentGroup.blog_post_id)
        .options(selectinload(BlogProtectedDocumentGroup.documents).selectinload(BlogProtectedDocument.media_file))
        .where(BlogPost.slug == blog_slug, BlogProtectedDocumentGroup.is_enabled.is_(True))
        .order_by(BlogProtectedDocumentGroup.sort_order, BlogProtectedDocumentGroup.title)
    ).all()

    result: list[ProtectedDocumentGroupOut] = []
    for group in groups:
        documents: list[ProtectedDocumentOut] = []
        for document in sorted(group.documents, key=lambda item: (item.sort_order, str(item.id))):
            media_file = document.media_file
            if media_file is None:
                continue
            download_filename = sanitize_public_download_filename(media_file.original_filename or media_file.stored_filename or media_file.object_key)
            fallback_title = media_file.title or media_file.original_filename or download_filename
            documents.append(
                ProtectedDocumentOut(
                    id=str(media_file.id),
                    title=_localized_text(document.title, document.title_nl, locale) or fallback_title,
                    file_name=media_file.original_filename,
                    mime_type=media_file.mime_type,
                    file_size_bytes=media_file.file_size_bytes,
                    download_url=build_protected_document_download_url(group.slug, media_file.id, download_filename),
                )
            )
        if not documents:
            continue
        result.append(
            ProtectedDocumentGroupOut(
                slug=group.slug,
                title=_localized_text(group.title, group.title_nl, locale) or 'Confidential documents',
                description=_localized_text(group.description, group.description_nl, locale)
                or 'These downloads are password-protected because they may contain confidential internship material.',
                documents=documents,
            )
        )
    return result


def build_protected_document_download_url(group_slug: str, media_id: UUID | str, filename: str | None) -> str:
    safe_filename = sanitize_public_download_filename(filename)
    return f'/api/public/protected-documents/{group_slug}/{media_id}/{safe_filename}'


def _token_signature(payload_b64: str) -> str:
    secret = get_settings().secret_key.encode('utf-8')
    return hmac.new(secret, payload_b64.encode('utf-8'), hashlib.sha256).hexdigest()


def _encode_token(*, group_slug: str, expires_at: int) -> str:
    payload = {'g': group_slug, 'exp': expires_at}
    payload_json = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    payload_b64 = base64.urlsafe_b64encode(payload_json).decode('ascii').rstrip('=')
    return f'{payload_b64}.{_token_signature(payload_b64)}'


def _decode_token(token: str) -> dict[str, object] | None:
    if not token or '.' not in token:
        return None
    payload_b64, signature = token.split('.', 1)
    if not hmac.compare_digest(_token_signature(payload_b64), signature):
        return None
    padding = '=' * (-len(payload_b64) % 4)
    try:
        payload = json.loads(base64.urlsafe_b64decode(f'{payload_b64}{padding}'))
    except (ValueError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def protected_document_cookie_name() -> str:
    return get_settings().protected_documents_cookie_name.strip() or 'portfolio_protected_documents'


def protected_document_cookie_path(group_slug: str) -> str:
    return f'/api/public/protected-documents/{group_slug}'


def set_protected_document_access_cookie(response: Response, *, group_slug: str) -> int:
    settings = get_settings()
    max_age_seconds = max(1, settings.protected_documents_access_ttl_minutes) * 60
    expires_at = int(time.time()) + max_age_seconds
    response.set_cookie(
        key=protected_document_cookie_name(),
        value=_encode_token(group_slug=group_slug, expires_at=expires_at),
        httponly=True,
        secure=settings.protected_documents_cookie_secure,
        samesite=_resolve_same_site_value(settings.protected_documents_cookie_same_site),
        path=protected_document_cookie_path(group_slug),
        max_age=max_age_seconds,
    )
    return max_age_seconds


def _resolve_same_site_value(value: str) -> str:
    normalized = value.strip().lower()
    return normalized if normalized in {'lax', 'strict', 'none'} else 'lax'


def protected_document_access_remaining_seconds(request: Request, *, group_slug: str) -> int:
    token = request.cookies.get(protected_document_cookie_name())
    payload = _decode_token(token or '')
    if not payload:
        return 0
    if payload.get('g') != group_slug:
        return 0
    expires_at = payload.get('exp')
    if not isinstance(expires_at, int):
        return 0
    return max(0, expires_at - int(time.time()))


def require_protected_document_access(request: Request, *, group_slug: str) -> None:
    if protected_document_access_remaining_seconds(request, group_slug=group_slug) <= 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Document access password required.')


def verify_protected_documents_password(group: BlogProtectedDocumentGroup, password: str) -> bool:
    candidate = password or ''
    if not group.password_hash:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Protected document password is not configured.')
    try:
        return verify_password(candidate, group.password_hash)
    except Exception:
        return False


def enforce_protected_document_unlock_rate_limit(request: Request, *, group_slug: str) -> None:
    settings = get_settings()
    identifier = _extract_request_ip(request) or 'anonymous'
    enforce_rate_limit_or_429(
        scope='protected-documents-unlock',
        identifier=f'{group_slug}:{identifier}',
        limit=settings.protected_documents_rate_limit_max_attempts,
        window_seconds=settings.protected_documents_rate_limit_window_seconds,
        detail='Too many document unlock attempts. Please wait before trying again.',
    )


def require_configured_group(session: Session, group_slug: str) -> BlogProtectedDocumentGroup:
    group = session.scalar(
        select(BlogProtectedDocumentGroup)
        .options(selectinload(BlogProtectedDocumentGroup.documents).selectinload(BlogProtectedDocument.media_file))
        .where(BlogProtectedDocumentGroup.slug == group_slug, BlogProtectedDocumentGroup.is_enabled.is_(True))
    )
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Protected document group not found.')
    return group


def ensure_media_belongs_to_group(group: BlogProtectedDocumentGroup, media_id: UUID) -> None:
    if media_id not in {document.media_file_id for document in group.documents}:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Protected document not found.')


def stream_protected_document(media_file: MediaFile, filename: str) -> Response:
    file_bytes = AdminMediaStorageService().download_object(bucket_name=media_file.bucket_name, object_key=media_file.object_key)
    download_filename = sanitize_public_download_filename(media_file.original_filename or filename or media_file.stored_filename)
    quoted_filename = _quote_filename(download_filename)
    fallback_filename = ''.join(character if ord(character) < 128 else '-' for character in download_filename) or PurePosixPath(filename).name or 'download'
    response = Response(content=file_bytes, media_type=media_file.mime_type or 'application/octet-stream')
    response.headers['Content-Disposition'] = f'attachment; filename="{fallback_filename}"; filename*=UTF-8\'\'{quoted_filename}'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
    response.headers['Cache-Control'] = 'private, no-store, max-age=0'
    return response


def _quote_filename(filename: str) -> str:
    from urllib.parse import quote

    return quote(filename)
