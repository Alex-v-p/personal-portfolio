from __future__ import annotations

from fastapi import HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import AdminSession, AdminUser
from app.domains.admin.repository.users import AdminUsersRepository
from app.domains.admin.schema import AdminAuthSessionOut, AdminLoginIn
from app.services.request_protection import _extract_request_ip, enforce_rate_limit_or_429
from app.services.security import (
    admin_session_max_age_seconds,
    clear_admin_session_cookie,
    create_admin_session_record,
    generate_admin_csrf_token,
    generate_admin_session_token,
    record_admin_auth_event,
    revoke_admin_session,
    rotate_admin_csrf_token,
    set_admin_session_cookie,
    verify_password,
)


class AdminAuthService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = AdminUsersRepository(session)
        self.settings = get_settings()

    def login(self, payload: AdminLoginIn, *, request: Request, response: Response) -> AdminAuthSessionOut:
        normalized_email = str(payload.email).strip().lower()
        self._enforce_login_rate_limits(request=request, email=normalized_email)

        admin_user = self.users.get_admin_user_by_email(normalized_email)
        if admin_user is None or not admin_user.is_active or not verify_password(payload.password, admin_user.password_hash):
            record_admin_auth_event(
                self.session,
                event_type='login',
                outcome='rejected',
                request=request,
                email=normalized_email,
                details={'reason': 'invalid_credentials'},
            )
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid admin email or password.')

        session_token = generate_admin_session_token()
        csrf_token = generate_admin_csrf_token()
        session_record = create_admin_session_record(
            self.session,
            admin_user=admin_user,
            session_token=session_token,
            csrf_token=csrf_token,
            request=request,
        )
        self.session.commit()
        self.session.refresh(session_record)

        set_admin_session_cookie(response, session_token, max_age_seconds=admin_session_max_age_seconds())
        record_admin_auth_event(
            self.session,
            event_type='login',
            outcome='accepted',
            request=request,
            admin_user=admin_user,
            email=admin_user.email,
            session_record=session_record,
            details={'ip': _extract_request_ip(request)},
        )
        return self._build_session_response(admin_user=admin_user, csrf_token=csrf_token)

    def build_authenticated_session(self, session_record: AdminSession) -> AdminAuthSessionOut:
        csrf_token = rotate_admin_csrf_token(self.session, session_record)
        return self._build_session_response(admin_user=session_record.admin_user, csrf_token=csrf_token)

    def logout(self, session_record: AdminSession | None, *, request: Request, response: Response) -> None:
        clear_admin_session_cookie(response)
        if session_record is None:
            return
        revoke_admin_session(self.session, session_record, reason='logout')
        record_admin_auth_event(
            self.session,
            event_type='logout',
            outcome='accepted',
            request=request,
            admin_user=session_record.admin_user,
            email=session_record.admin_user.email,
            session_record=session_record,
        )

    def _build_session_response(self, *, admin_user: AdminUser, csrf_token: str) -> AdminAuthSessionOut:
        return AdminAuthSessionOut(
            csrf_token=csrf_token,
            expires_in_seconds=admin_session_max_age_seconds(),
            user=self.users.map_admin_user(admin_user),
        )

    def _enforce_login_rate_limits(self, *, request: Request, email: str) -> None:
        ip_identifier = _extract_request_ip(request) or 'anonymous'
        detail = 'Too many admin login attempts. Please wait before trying again.'
        enforce_rate_limit_or_429(
            scope='admin-login-ip',
            identifier=ip_identifier,
            limit=self.settings.admin_login_rate_limit_max_attempts,
            window_seconds=self.settings.admin_login_rate_limit_window_seconds,
            detail=detail,
        )
        enforce_rate_limit_or_429(
            scope='admin-login-email',
            identifier=email,
            limit=self.settings.admin_login_rate_limit_max_attempts,
            window_seconds=self.settings.admin_login_rate_limit_window_seconds,
            detail=detail,
        )
