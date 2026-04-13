from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select

from app.db.models import AdminUser
from app.schemas.admin import AdminUserCreateIn, AdminUserOut, AdminUserUpdateIn
from app.repositories.admin.support import AdminRepositorySupport
from app.services.security import hash_password


class AdminUsersRepository(AdminRepositorySupport):
    def get_admin_user_by_email(self, email: str) -> AdminUser | None:
        return self.session.scalar(select(AdminUser).where(func.lower(AdminUser.email) == email.strip().lower()))

    def list_admin_users(self) -> list[AdminUserOut]:
        users = self.session.scalars(select(AdminUser).order_by(AdminUser.created_at.desc(), AdminUser.email.asc())).all()
        return [self.map_admin_user(user) for user in users]

    def create_admin_user(self, payload: AdminUserCreateIn) -> AdminUserOut:
        user = AdminUser(
            email=str(payload.email).strip().lower(),
            display_name=payload.display_name.strip(),
            password_hash=hash_password(payload.password),
            is_active=payload.is_active,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return self.map_admin_user(user)

    def update_admin_user(self, admin_user_id: UUID, payload: AdminUserUpdateIn) -> AdminUserOut | None:
        user = self.session.get(AdminUser, admin_user_id)
        if user is None:
            return None
        user.email = str(payload.email).strip().lower()
        user.display_name = payload.display_name.strip()
        user.is_active = payload.is_active
        if payload.password:
            user.password_hash = hash_password(payload.password)
        self.session.commit()
        self.session.refresh(user)
        return self.map_admin_user(user)

    def delete_admin_user(self, admin_user_id: UUID) -> bool:
        user = self.session.get(AdminUser, admin_user_id)
        if user is None:
            return False
        self.session.delete(user)
        self.session.commit()
        return True
