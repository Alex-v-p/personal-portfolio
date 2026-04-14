from __future__ import annotations

from app.db.models import AdminUser
from app.domains.admin.schema import AdminUserOut


class AdminRepositoryUserMappingMixin:
    def map_admin_user(self, admin_user: AdminUser) -> AdminUserOut:
        return AdminUserOut(
            id=str(admin_user.id),
            email=admin_user.email,
            display_name=admin_user.display_name,
            is_active=admin_user.is_active,
            created_at=admin_user.created_at.isoformat(),
        )
