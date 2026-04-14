from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import AdminAuthEvent, AdminSession, AdminUser
from app.db.session import get_session
from app.services.request_protection import _extract_request_ip
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
SAFE_HTTP_METHODS = {'GET', 'HEAD', 'OPTIONS'}
SESSION_TOUCH_INTERVAL_SECONDS = 60


class AdminTokenError(HTTPException):
    def __init__(self, detail: str = 'Admin authentication required.') -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)



def hash_password(password: str) -> str:
    return pwd_context.hash(password)



def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)



def generate_admin_session_token() -> str:
    return secrets.token_urlsafe(48)



def generate_admin_csrf_token() -> str:
    return secrets.token_urlsafe(32)



def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()



def admin_session_expires_at(*, now: datetime | None = None) -> datetime:
    settings = get_settings()
    effective_now = now or datetime.now(UTC)
    return effective_now + timedelta(minutes=settings.admin_session_max_age_minutes)



def admin_session_max_age_seconds() -> int:
    settings = get_settings()
    return settings.admin_session_max_age_minutes * 60



def admin_session_idle_timeout_seconds() -> int:
    settings = get_settings()
    return settings.admin_session_idle_timeout_minutes * 60



def _admin_cookie_path() -> str:
    return '/api/admin'



def _request_origin_allowed(request: Request) -> bool:
    origin = request.headers.get('origin')
    if not origin:
        return True
    settings = get_settings()
    allowed = {item.rstrip('/') for item in settings.cors_allowed_origins_list}
    allowed.add(str(request.base_url).rstrip('/'))
    return origin.rstrip('/') in allowed



def _resolve_same_site_value() -> str:
    value = get_settings().admin_session_cookie_same_site.strip().lower() or 'lax'
    if value not in {'lax', 'strict', 'none'}:
        return 'lax'
    return value



def set_admin_session_cookie(response: Response, session_token: str, *, max_age_seconds: int | None = None) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.admin_session_cookie_name,
        value=session_token,
        httponly=True,
        secure=settings.admin_session_cookie_secure,
        samesite=_resolve_same_site_value(),
        path=_admin_cookie_path(),
        max_age=max_age_seconds or admin_session_max_age_seconds(),
    )



def clear_admin_session_cookie(response: Response) -> None:
    settings = get_settings()
    response.delete_cookie(
        key=settings.admin_session_cookie_name,
        path=_admin_cookie_path(),
        secure=settings.admin_session_cookie_secure,
        samesite=_resolve_same_site_value(),
    )



def get_admin_session_cookie_value(request: Request) -> str | None:
    cookie_name = get_settings().admin_session_cookie_name
    cookie_value = request.cookies.get(cookie_name)
    if cookie_value and cookie_value.strip():
        return cookie_value.strip()
    return None



def create_admin_session_record(
    db: Session,
    *,
    admin_user: AdminUser,
    session_token: str,
    csrf_token: str,
    request: Request | None,
    now: datetime | None = None,
) -> AdminSession:
    effective_now = now or datetime.now(UTC)
    ip_address = _extract_request_ip(request)
    user_agent = request.headers.get('user-agent')[:500] if request is not None and request.headers.get('user-agent') else None
    record = AdminSession(
        admin_user_id=admin_user.id,
        session_token_hash=_hash_token(session_token),
        csrf_token_hash=_hash_token(csrf_token),
        expires_at=admin_session_expires_at(now=effective_now),
        last_seen_at=effective_now,
        created_at=effective_now,
        updated_at=effective_now,
        created_ip=ip_address[:64] if ip_address else None,
        last_seen_ip=ip_address[:64] if ip_address else None,
        user_agent=user_agent,
    )
    db.add(record)
    return record



def rotate_admin_csrf_token(db: Session, record: AdminSession) -> str:
    new_token = generate_admin_csrf_token()
    record.csrf_token_hash = _hash_token(new_token)
    record.updated_at = datetime.now(UTC)
    db.add(record)
    db.commit()
    db.refresh(record)
    return new_token



def revoke_admin_session(db: Session, record: AdminSession, *, reason: str) -> None:
    if record.revoked_at is not None:
        return
    record.revoked_at = datetime.now(UTC)
    record.revoke_reason = reason[:120]
    db.add(record)
    db.commit()



def record_admin_auth_event(
    db: Session,
    *,
    event_type: str,
    outcome: str,
    request: Request | None,
    admin_user: AdminUser | None = None,
    email: str | None = None,
    details: dict[str, Any] | None = None,
    session_record: AdminSession | None = None,
) -> None:
    ip_address = _extract_request_ip(request)
    user_agent = request.headers.get('user-agent')[:500] if request is not None and request.headers.get('user-agent') else None
    event = AdminAuthEvent(
        admin_user_id=admin_user.id if admin_user is not None else None,
        event_type=event_type[:80],
        outcome=outcome[:40],
        email=email[:320] if email else None,
        ip_address=ip_address[:64] if ip_address else None,
        user_agent=user_agent,
        details=details,
        session_id=session_record.id if session_record is not None else None,
        session_label=str(session_record.id) if session_record is not None else None,
    )
    db.add(event)
    db.commit()



def _invalidate_session_if_needed(db: Session, record: AdminSession, *, now: datetime) -> None:
    idle_cutoff = now - timedelta(seconds=admin_session_idle_timeout_seconds())
    if record.revoked_at is not None:
        raise AdminTokenError('Admin session is no longer active.')
    if record.expires_at <= now:
        revoke_admin_session(db, record, reason='expired')
        raise AdminTokenError('Admin session has expired. Please sign in again.')
    if record.last_seen_at <= idle_cutoff:
        revoke_admin_session(db, record, reason='idle-timeout')
        raise AdminTokenError('Admin session timed out due to inactivity. Please sign in again.')



def _touch_session(db: Session, record: AdminSession, *, request: Request | None, now: datetime) -> None:
    ip_address = _extract_request_ip(request)
    should_touch = (now - record.last_seen_at).total_seconds() >= SESSION_TOUCH_INTERVAL_SECONDS
    if not should_touch and ip_address == record.last_seen_ip:
        return
    record.last_seen_at = now
    record.updated_at = now
    if ip_address:
        record.last_seen_ip = ip_address[:64]
    db.add(record)
    db.commit()



def resolve_current_admin_session(db: Session, request: Request, *, touch: bool = True) -> AdminSession:
    cached = getattr(request.state, 'admin_session_record', None)
    if cached is not None:
        return cached

    session_token = get_admin_session_cookie_value(request)
    if not session_token:
        raise AdminTokenError()

    record = db.scalar(select(AdminSession).where(AdminSession.session_token_hash == _hash_token(session_token)))
    if record is None:
        raise AdminTokenError()

    now = datetime.now(UTC)
    _invalidate_session_if_needed(db, record, now=now)
    admin_user = record.admin_user
    if admin_user is None or not admin_user.is_active:
        revoke_admin_session(db, record, reason='admin-inactive')
        raise AdminTokenError('Admin account not found or inactive.')

    if touch:
        _touch_session(db, record, request=request, now=now)

    request.state.admin_session_record = record
    request.state.admin_user_record = admin_user
    return record



def get_current_admin_session(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> AdminSession:
    return resolve_current_admin_session(session, request, touch=True)



def get_current_admin_user(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> AdminUser:
    if getattr(request.state, 'admin_user_record', None) is not None:
        return request.state.admin_user_record
    record = resolve_current_admin_session(session, request, touch=True)
    return record.admin_user



def require_admin_csrf(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> None:
    if not request.url.path.startswith('/api/admin'):
        return
    if request.method.upper() in SAFE_HTTP_METHODS:
        return
    if request.url.path.endswith('/auth/login'):
        return
    if not _request_origin_allowed(request):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin request origin is not allowed.')

    record = resolve_current_admin_session(session, request, touch=False)
    header_name = get_settings().admin_csrf_header_name
    csrf_token = request.headers.get(header_name)
    if not csrf_token or not secrets.compare_digest(record.csrf_token_hash, _hash_token(csrf_token)):
        record_admin_auth_event(
            session,
            event_type='csrf_validation',
            outcome='rejected',
            request=request,
            admin_user=record.admin_user,
            details={'reason': 'missing_or_invalid_csrf'},
            session_record=record,
        )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin CSRF validation failed.')


__all__ = [
    'AdminTokenError',
    'admin_session_idle_timeout_seconds',
    'admin_session_max_age_seconds',
    'clear_admin_session_cookie',
    'create_admin_session_record',
    'generate_admin_csrf_token',
    'generate_admin_session_token',
    'get_admin_session_cookie_value',
    'get_current_admin_session',
    'get_current_admin_user',
    'hash_password',
    'record_admin_auth_event',
    'require_admin_csrf',
    'revoke_admin_session',
    'rotate_admin_csrf_token',
    'set_admin_session_cookie',
    'verify_password',
]
