from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import AdminSession
from app.domains.admin.repository.users import AdminUsersRepository
from app.domains.admin.schema import (
    AdminAuthSessionOut,
    AdminLoginIn,
    AdminMfaSetupConfirmIn,
    AdminMfaSetupConfirmOut,
    AdminMfaSetupStartOut,
    AdminMfaVerifyIn,
)
from app.services.request_protection import _extract_request_ip, enforce_rate_limit_or_429
from app.services.security import (
    admin_session_max_age_seconds,
    build_admin_totp_uri,
    clear_admin_session_cookie,
    clear_admin_session_pending_mfa_secret,
    consume_admin_backup_code,
    create_admin_session_record,
    generate_admin_backup_codes,
    generate_admin_csrf_token,
    generate_admin_session_token,
    generate_admin_totp_qr_code_data_url,
    generate_admin_totp_secret,
    get_admin_session_pending_mfa_secret,
    hash_admin_backup_code,
    get_admin_totp_issuer,
    mark_admin_session_mfa_complete,
    record_admin_auth_event,
    revoke_admin_session,
    rotate_admin_csrf_token,
    set_admin_session_cookie,
    set_admin_session_pending_mfa_secret,
    verify_admin_totp_code,
    verify_password,
    encrypt_admin_secret,
    decrypt_admin_secret,
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
            details={'ip': _extract_request_ip(request), 'mfa_enabled': admin_user.mfa_enabled},
        )
        return self._build_session_response(session_record=session_record, csrf_token=csrf_token)

    def build_authenticated_session(self, session_record: AdminSession) -> AdminAuthSessionOut:
        csrf_token = rotate_admin_csrf_token(self.session, session_record)
        return self._build_session_response(session_record=session_record, csrf_token=csrf_token)

    def begin_mfa_setup(self, session_record: AdminSession, *, request: Request) -> AdminMfaSetupStartOut:
        admin_user = session_record.admin_user
        if admin_user.mfa_enabled:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Admin MFA is already configured for this account.')
        secret = generate_admin_totp_secret()
        set_admin_session_pending_mfa_secret(self.session, session_record, secret=secret)
        otpauth_uri = build_admin_totp_uri(secret=secret, email=admin_user.email)
        record_admin_auth_event(
            self.session,
            event_type='mfa_setup_started',
            outcome='accepted',
            request=request,
            admin_user=admin_user,
            email=admin_user.email,
            session_record=session_record,
        )
        return AdminMfaSetupStartOut(
            manual_entry_key=secret,
            otpauth_uri=otpauth_uri,
            qr_code_data_url=generate_admin_totp_qr_code_data_url(otpauth_uri),
            issuer=get_admin_totp_issuer(),
        )

    def confirm_mfa_setup(
        self,
        session_record: AdminSession,
        payload: AdminMfaSetupConfirmIn,
        *,
        request: Request,
    ) -> AdminMfaSetupConfirmOut:
        admin_user = session_record.admin_user
        if admin_user.mfa_enabled:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Admin MFA is already configured for this account.')
        secret = get_admin_session_pending_mfa_secret(session_record)
        if not secret:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Start MFA setup again before confirming the authenticator code.')
        if not verify_admin_totp_code(secret, payload.code):
            record_admin_auth_event(
                self.session,
                event_type='mfa_setup_confirmed',
                outcome='rejected',
                request=request,
                admin_user=admin_user,
                email=admin_user.email,
                session_record=session_record,
                details={'reason': 'invalid_totp_code'},
            )
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The authenticator code was not valid. Please try again.')

        backup_codes = generate_admin_backup_codes()
        now = datetime.now(UTC)
        admin_user.mfa_enabled = True
        admin_user.mfa_totp_secret_encrypted = encrypt_admin_secret(secret)
        admin_user.mfa_enrolled_at = now
        admin_user.mfa_recovery_codes_hashes = [hash_admin_backup_code(code) for code in backup_codes]
        self.session.add(admin_user)
        self.session.commit()
        self.session.refresh(admin_user)
        clear_admin_session_pending_mfa_secret(self.session, session_record)
        mark_admin_session_mfa_complete(self.session, session_record, now=now)
        record_admin_auth_event(
            self.session,
            event_type='mfa_setup_confirmed',
            outcome='accepted',
            request=request,
            admin_user=admin_user,
            email=admin_user.email,
            session_record=session_record,
            details={'recovery_code_count': len(backup_codes)},
        )
        return AdminMfaSetupConfirmOut(
            backup_codes=backup_codes,
            session=self.build_authenticated_session(session_record),
        )

    def verify_mfa(self, session_record: AdminSession, payload: AdminMfaVerifyIn, *, request: Request) -> AdminAuthSessionOut:
        admin_user = session_record.admin_user
        if not admin_user.mfa_enabled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Admin MFA setup is required for this account before verification.')

        if payload.code:
            secret = admin_user.mfa_totp_secret_encrypted
            if not secret or not verify_admin_totp_code(decrypt_admin_secret(secret) or '', payload.code):
                record_admin_auth_event(
                    self.session,
                    event_type='mfa_verified',
                    outcome='rejected',
                    request=request,
                    admin_user=admin_user,
                    email=admin_user.email,
                    session_record=session_record,
                    details={'method': 'totp', 'reason': 'invalid_code'},
                )
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The authenticator code was not valid. Please try again.')
            method = 'totp'
        else:
            if not consume_admin_backup_code(admin_user, payload.recovery_code or ''):
                record_admin_auth_event(
                    self.session,
                    event_type='mfa_verified',
                    outcome='rejected',
                    request=request,
                    admin_user=admin_user,
                    email=admin_user.email,
                    session_record=session_record,
                    details={'method': 'recovery-code', 'reason': 'invalid_code'},
                )
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='That recovery code was not valid. Please try again.')
            self.session.add(admin_user)
            self.session.commit()
            self.session.refresh(admin_user)
            method = 'recovery-code'

        mark_admin_session_mfa_complete(self.session, session_record)
        record_admin_auth_event(
            self.session,
            event_type='mfa_verified',
            outcome='accepted',
            request=request,
            admin_user=admin_user,
            email=admin_user.email,
            session_record=session_record,
            details={'method': method},
        )
        return self.build_authenticated_session(session_record)

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

    def _build_session_response(self, *, session_record: AdminSession, csrf_token: str) -> AdminAuthSessionOut:
        admin_user = session_record.admin_user
        is_mfa_verified = session_record.mfa_completed_at is not None
        is_mfa_enabled = admin_user.mfa_enabled
        return AdminAuthSessionOut(
            csrf_token=csrf_token,
            expires_in_seconds=admin_session_max_age_seconds(),
            user=self.users.map_admin_user(admin_user),
            is_mfa_enabled=is_mfa_enabled,
            is_mfa_verified=is_mfa_verified,
            mfa_required=is_mfa_enabled and not is_mfa_verified,
            mfa_setup_required=not is_mfa_enabled,
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
