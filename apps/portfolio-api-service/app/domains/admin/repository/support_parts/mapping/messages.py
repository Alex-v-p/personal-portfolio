from __future__ import annotations

from app.db.models import ContactMessage
from app.domains.admin.schema import AdminContactMessageOut


class AdminRepositoryMessagesMappingMixin:
    def _map_contact_message(self, message: ContactMessage) -> AdminContactMessageOut:
        return AdminContactMessageOut(
            id=str(message.id),
            name=message.name,
            email=message.email,
            subject=message.subject,
            message=message.message,
            source_page=message.source_page,
            is_read=message.is_read,
            created_at=message.created_at.isoformat(),
            updated_at=message.updated_at.isoformat(),
        )
