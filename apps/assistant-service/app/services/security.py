from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_session


class AdminTokenError(HTTPException):
    def __init__(self, detail: str = 'Admin authentication is required.') -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers={'WWW-Authenticate': 'Bearer'})


bearer_scheme = HTTPBearer(auto_error=False)


def decode_admin_access_token(token: str) -> dict:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
    except JWTError as exc:
        raise AdminTokenError('Admin token is invalid or expired.') from exc

    if payload.get('type') != 'admin-access':
        raise AdminTokenError('Admin token is invalid.')
    return payload


def get_current_admin_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    session: Session = Depends(get_session),
) -> dict:
    if credentials is None:
        raise AdminTokenError()

    payload = decode_admin_access_token(credentials.credentials)
    admin_id = payload.get('sub')
    if not admin_id:
        raise AdminTokenError('Admin token payload is missing the subject.')

    try:
        admin_uuid = str(UUID(str(admin_id)))
    except ValueError as exc:
        raise AdminTokenError('Admin token subject is invalid.') from exc

    admin_user = session.execute(
        text(
            'SELECT id, email, display_name, is_active '
            'FROM admin_users '
            'WHERE id = :admin_id'
        ),
        {'admin_id': admin_uuid},
    ).mappings().first()

    if admin_user is None or not bool(admin_user['is_active']):
        raise AdminTokenError('Admin user is no longer active.')

    return dict(admin_user)