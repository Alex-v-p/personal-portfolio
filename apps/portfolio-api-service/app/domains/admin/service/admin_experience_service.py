from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.admin.repository.content import AdminContentManagementRepository
from app.domains.admin.schema import AdminExperienceOut, AdminExperiencesListOut, AdminExperienceUpsertIn


class AdminExperienceService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminContentManagementRepository(session)

    def list_experiences(self) -> AdminExperiencesListOut:
        items = self.repository.list_experiences()
        return AdminExperiencesListOut(items=items, total=len(items))

    def get_experience(self, experience_id: UUID) -> AdminExperienceOut:
        experience = self.repository.get_experience(experience_id)
        if experience is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Experience entry not found.')
        return experience

    def create_experience(self, payload: AdminExperienceUpsertIn) -> AdminExperienceOut:
        return self.repository.create_experience(payload)

    def update_experience(self, experience_id: UUID, payload: AdminExperienceUpsertIn) -> AdminExperienceOut:
        experience = self.repository.update_experience(experience_id, payload)
        if experience is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Experience entry not found.')
        return experience

    def delete_experience(self, experience_id: UUID) -> None:
        deleted = self.repository.delete_experience(experience_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Experience entry not found.')
