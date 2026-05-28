from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.admin.repository.activity import AdminActivityRepository
from app.domains.admin.schema import AdminContactMessageOut, AdminContactMessagesListOut, AdminSiteActivityOut


class AdminActivityService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminActivityRepository(session)

    def get_site_activity(self) -> AdminSiteActivityOut:
        return self.repository.get_site_activity()

    def list_contact_messages(self) -> AdminContactMessagesListOut:
        items = self.repository.list_contact_messages()
        return AdminContactMessagesListOut(items=items, total=len(items))

    def update_contact_message_status(self, message_id: UUID, *, is_read: bool) -> AdminContactMessageOut:
        message = self.repository.update_contact_message_status(message_id, is_read=is_read)
        if message is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact message not found.')
        return message
