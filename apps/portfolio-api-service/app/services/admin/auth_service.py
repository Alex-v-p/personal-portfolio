from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.admin.users import AdminUsersRepository
from app.schemas.admin import AdminAuthTokenOut, AdminLoginIn
from app.services.security import create_admin_access_token, verify_password


class AdminAuthService:
    def __init__(self, session: Session) -> None:
        self.users = AdminUsersRepository(session)

    def login(self, payload: AdminLoginIn) -> AdminAuthTokenOut:
        admin_user = self.users.get_admin_user_by_email(payload.email)
        if admin_user is None or not admin_user.is_active or not verify_password(payload.password, admin_user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid admin email or password.')
        token, expires_in_seconds = create_admin_access_token(admin_user=admin_user)
        return AdminAuthTokenOut(
            access_token=token,
            expires_in_seconds=expires_in_seconds,
            user=self.users.map_admin_user(admin_user),
        )
