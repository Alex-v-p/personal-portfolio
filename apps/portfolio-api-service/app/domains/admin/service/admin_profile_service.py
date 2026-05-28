from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.admin.repository.content import AdminContentManagementRepository
from app.domains.admin.schema import AdminProfileOut, AdminProfileUpdateIn


class AdminProfileService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminContentManagementRepository(session)

    def get_profile(self) -> AdminProfileOut:
        profile = self.repository.get_profile()
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Profile not found.')
        return profile

    def update_profile(self, payload: AdminProfileUpdateIn) -> AdminProfileOut:
        profile = self.repository.update_profile(payload)
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Profile not found.')
        return profile
