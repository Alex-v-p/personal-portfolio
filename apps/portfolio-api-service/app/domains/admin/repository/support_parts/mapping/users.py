from __future__ import annotations

from app.db.models import AdminUser
from app.domains.admin.schema import AdminUserOut


class AdminRepositoryUserMappingMixin:
    def map_admin_user(self, admin_user: AdminUser) -> AdminUserOut:
        recovery_codes = admin_user.mfa_recovery_codes_hashes or []
        return AdminUserOut(
            id=str(admin_user.id),
            email=admin_user.email,
            display_name=admin_user.display_name,
            is_active=admin_user.is_active,
            created_at=admin_user.created_at.isoformat(),
            mfa_enabled=admin_user.mfa_enabled,
            mfa_enrolled_at=admin_user.mfa_enrolled_at.isoformat() if admin_user.mfa_enrolled_at else None,
            mfa_recovery_codes_remaining=len(recovery_codes),
        )
