from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import ContactMessage
from app.schemas.contact import ContactMessageIn, ContactMessageOut


class ContactMessageRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: ContactMessageIn) -> ContactMessageOut:
        item = ContactMessage(
            name=payload.name,
            email=str(payload.email),
            subject=payload.subject,
            message=payload.message,
            source_page=payload.source_page,
            is_read=False,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return ContactMessageOut.model_validate(
            {
                'id': str(item.id),
                'name': item.name,
                'email': item.email,
                'subject': item.subject,
                'message': item.message,
                'source_page': item.source_page,
                'is_read': item.is_read,
                'created_at': item.created_at.isoformat(),
                'updated_at': item.updated_at.isoformat(),
            }
        )
