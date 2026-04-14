from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.admin.repository.content import AdminContentManagementRepository
from app.domains.admin.schema import AdminProjectOut, AdminProjectsListOut, AdminProjectUpsertIn


class AdminProjectsService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminContentManagementRepository(session)

    def list_projects(self) -> AdminProjectsListOut:
        items = self.repository.list_projects()
        return AdminProjectsListOut(items=items, total=len(items))

    def get_project(self, project_id: UUID) -> AdminProjectOut:
        project = self.repository.get_project(project_id)
        if project is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found.')
        return project

    def create_project(self, payload: AdminProjectUpsertIn) -> AdminProjectOut:
        return self.repository.create_project(payload)

    def update_project(self, project_id: UUID, payload: AdminProjectUpsertIn) -> AdminProjectOut:
        project = self.repository.update_project(project_id, payload)
        if project is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found.')
        return project

    def delete_project(self, project_id: UUID) -> None:
        deleted = self.repository.delete_project(project_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found.')
