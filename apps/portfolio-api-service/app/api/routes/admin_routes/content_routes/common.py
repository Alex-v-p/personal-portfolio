from __future__ import annotations

from app.api.routes.admin_routes.common import SessionDep
from app.repositories.admin.content import AdminContentManagementRepository


def repository(session: SessionDep) -> AdminContentManagementRepository:
    return AdminContentManagementRepository(session)
