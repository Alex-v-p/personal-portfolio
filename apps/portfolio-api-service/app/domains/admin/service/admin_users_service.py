from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.admin.repository.users import AdminUsersRepository
from app.domains.admin.schema import AdminUserCreateIn, AdminUserOut, AdminUserUpdateIn


class AdminUsersService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminUsersRepository(session)

    def list_admin_users(self) -> list[AdminUserOut]:
        return self.repository.list_admin_users()

    def create_admin_user(self, payload: AdminUserCreateIn) -> AdminUserOut:
        return self.repository.create_admin_user(payload)

    def update_admin_user(self, admin_user_id: UUID, payload: AdminUserUpdateIn) -> AdminUserOut:
        user = self.repository.update_admin_user(admin_user_id, payload)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Admin user not found.')
        return user

    def delete_admin_user(self, admin_user_id: UUID, *, current_admin_id: UUID) -> None:
        if current_admin_id == admin_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You cannot delete the currently signed-in admin user.')
        deleted = self.repository.delete_admin_user(admin_user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Admin user not found.')
