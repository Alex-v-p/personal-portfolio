from __future__ import annotations

from pathlib import PurePosixPath
from typing import Literal
from urllib.parse import quote
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy.orm import Session

from app.db.models import MediaFile, MediaVisibility
from app.db.session import get_session
from app.domains.public_site.repository import DEFAULT_PUBLIC_LOCALE, PublicLocale
from app.domains.public_site.schema import (
    BlogPostDetailOut,
    BlogPostsListOut,
    ExperienceListOut,
    GithubSnapshotOut,
    HomeOut,
    NavigationListOut,
    ProfileOut,
    ProjectDetailOut,
    ProtectedDocumentsAccessOut,
    ProtectedDocumentsUnlockIn,
    ProtectedDocumentsUnlockOut,
    ProjectsListOut,
    SiteShellOut,
    StatsOut,
)
from app.domains.public_site.service.public_content_query_service import PublicContentQueryService
from app.domains.media.service.resolver import sanitize_public_download_filename
from app.domains.media.service.storage import AdminMediaStorageService
from app.domains.public_site.protected_documents import (
    enforce_protected_document_unlock_rate_limit,
    ensure_media_belongs_to_group,
    protected_document_access_remaining_seconds,
    require_configured_group,
    require_protected_document_access,
    set_protected_document_access_cookie,
    stream_protected_document,
    verify_protected_documents_password,
)

router = APIRouter()


def resolve_public_locale(locale: PublicLocale = Query(default=DEFAULT_PUBLIC_LOCALE)) -> PublicLocale:
    return locale



@router.get('/protected-documents/{group_slug}/access', response_model=ProtectedDocumentsAccessOut)
def get_protected_document_access(group_slug: str, request: Request, session: Session = Depends(get_session)) -> ProtectedDocumentsAccessOut:
    require_configured_group(session, group_slug)
    remaining_seconds = protected_document_access_remaining_seconds(request, group_slug=group_slug)
    return ProtectedDocumentsAccessOut(unlocked=remaining_seconds > 0, expires_in_seconds=remaining_seconds)


@router.post('/protected-documents/{group_slug}/unlock', response_model=ProtectedDocumentsUnlockOut)
def unlock_protected_documents(group_slug: str, payload: ProtectedDocumentsUnlockIn, request: Request, response: Response, session: Session = Depends(get_session)) -> ProtectedDocumentsUnlockOut:
    group = require_configured_group(session, group_slug)
    enforce_protected_document_unlock_rate_limit(request, group_slug=group_slug)

    if not verify_protected_documents_password(group, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid document access password.')

    max_age_seconds = set_protected_document_access_cookie(response, group_slug=group_slug)
    return ProtectedDocumentsUnlockOut(unlocked=True, expires_in_seconds=max_age_seconds)


@router.get('/protected-documents/{group_slug}/{media_id}/{filename}', response_model=None)
def download_protected_document(group_slug: str, media_id: UUID, filename: str, request: Request, session: Session = Depends(get_session)) -> Response:
    group = require_configured_group(session, group_slug)
    ensure_media_belongs_to_group(group, media_id)
    require_protected_document_access(request, group_slug=group_slug)

    media_file = session.get(MediaFile, media_id)
    if media_file is None:
        raise HTTPException(status_code=404, detail='Protected document not found.')

    return stream_protected_document(media_file, filename)


@router.get('/media-files/{media_id}/{filename}', response_model=None)
def download_public_media_file(
    media_id: UUID,
    filename: str,
    disposition: Literal['attachment', 'inline'] = Query(default='attachment'),
    session: Session = Depends(get_session),
) -> Response:
    media_file = session.get(MediaFile, media_id)
    if media_file is None or media_file.visibility != MediaVisibility.PUBLIC:
        raise HTTPException(status_code=404, detail='Media file not found.')

    file_bytes = AdminMediaStorageService().download_object(bucket_name=media_file.bucket_name, object_key=media_file.object_key)
    download_filename = sanitize_public_download_filename(filename or media_file.original_filename or media_file.stored_filename)
    quoted_filename = quote(download_filename)
    fallback_filename = ''.join(character if ord(character) < 128 else '-' for character in download_filename) or PurePosixPath(filename).name or 'download'

    response = Response(content=file_bytes, media_type=media_file.mime_type or 'application/octet-stream')
    response.headers['Content-Disposition'] = f"{disposition}; filename=\"{fallback_filename}\"; filename*=UTF-8''{quoted_filename}"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@router.get('/profile', response_model=ProfileOut)
def get_profile(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> ProfileOut:
    return PublicContentQueryService(session, locale=locale).get_profile()


@router.get('/navigation', response_model=NavigationListOut)
def get_navigation(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> NavigationListOut:
    return PublicContentQueryService(session, locale=locale).list_navigation()


@router.get('/site-shell', response_model=SiteShellOut)
def get_site_shell(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> SiteShellOut:
    return PublicContentQueryService(session, locale=locale).get_site_shell()


@router.get('/home', response_model=HomeOut)
def get_home(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> HomeOut:
    return PublicContentQueryService(session, locale=locale).get_home()


@router.get('/projects', response_model=ProjectsListOut)
def list_projects(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> ProjectsListOut:
    return PublicContentQueryService(session, locale=locale).list_projects()


@router.get('/projects/{slug}', response_model=ProjectDetailOut)
def get_project(slug: str, locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> ProjectDetailOut:
    return PublicContentQueryService(session, locale=locale).get_project(slug)


@router.get('/blog-posts', response_model=BlogPostsListOut)
def list_blog_posts(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> BlogPostsListOut:
    return PublicContentQueryService(session, locale=locale).list_blog_posts()


@router.get('/blog-posts/{slug}', response_model=BlogPostDetailOut)
def get_blog_post(slug: str, locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> BlogPostDetailOut:
    return PublicContentQueryService(session, locale=locale).get_blog_post(slug)


@router.get('/experience', response_model=ExperienceListOut)
def list_experience(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> ExperienceListOut:
    return PublicContentQueryService(session, locale=locale).list_experience()


@router.get('/github', response_model=GithubSnapshotOut)
def get_github_snapshot(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> GithubSnapshotOut:
    return PublicContentQueryService(session, locale=locale).get_github_snapshot()


@router.get('/stats', response_model=StatsOut)
def get_stats(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> StatsOut:
    return PublicContentQueryService(session, locale=locale).get_stats()
