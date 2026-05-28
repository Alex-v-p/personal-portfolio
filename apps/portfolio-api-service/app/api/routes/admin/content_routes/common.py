from __future__ import annotations

from app.api.routes.admin.common import SessionDep
from app.domains.admin.repository.content import AdminContentManagementRepository


def repository(session: SessionDep) -> AdminContentManagementRepository:
    return AdminContentManagementRepository(session)
