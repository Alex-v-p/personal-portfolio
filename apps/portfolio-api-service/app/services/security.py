from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import AdminUser
from app.db.session import get_session

pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
bearer_scheme = HTTPBearer(auto_error=False)


class AdminTokenError(HTTPException):
    def __init__(self, detail: str = 'Admin authentication required.') -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)



def hash_password(password: str) -> str:
    return pwd_context.hash(password)



def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)



def create_admin_access_token(*, admin_user: AdminUser, expires_minutes: int | None = None) -> tuple[str, int]:
    settings = get_settings()
    lifetime_minutes = expires_minutes or settings.admin_access_token_expire_minutes
    expires_at = datetime.now(UTC) + timedelta(minutes=lifetime_minutes)
    payload = {
        'sub': str(admin_user.id),
        'email': admin_user.email,
        'type': 'admin-access',
        'exp': expires_at,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm='HS256')
    return token, lifetime_minutes * 60



def decode_admin_access_token(token: str) -> dict:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
    except JWTError as exc:  # pragma: no cover - jose internals are already tested upstream
        raise AdminTokenError('Admin token is invalid or expired.') from exc

    if payload.get('type') != 'admin-access':
        raise AdminTokenError('Admin token is invalid.')
    return payload



def get_current_admin_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    session: Annotated[Session, Depends(get_session)],
) -> AdminUser:
    if credentials is None or credentials.scheme.lower() != 'bearer':
        raise AdminTokenError()

    payload = decode_admin_access_token(credentials.credentials)
    admin_id = payload.get('sub')
    if not admin_id:
        raise AdminTokenError('Admin token payload is missing the subject.')

    try:
        admin_uuid = UUID(str(admin_id))
    except ValueError as exc:
        raise AdminTokenError('Admin token subject is invalid.') from exc

    admin_user = session.get(AdminUser, admin_uuid)
    if admin_user is None or not admin_user.is_active:
        raise AdminTokenError('Admin account not found or inactive.')

    return admin_user
