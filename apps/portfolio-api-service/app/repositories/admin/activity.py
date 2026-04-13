from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import AssistantConversation, ContactMessage, EventType, SiteEvent
from app.schemas.admin import AdminContactMessageOut, AdminSiteActivityOut, AdminSiteActivitySummaryOut
from app.repositories.admin.support import AdminRepositorySupport


class AdminActivityRepository(AdminRepositorySupport):
    def list_contact_messages(self) -> list[AdminContactMessageOut]:
        messages = self.session.scalars(select(ContactMessage).order_by(ContactMessage.created_at.desc())).all()
        return [self._map_contact_message(message) for message in messages]

    def get_site_activity(self) -> AdminSiteActivityOut:
        events = self.session.scalars(
            select(SiteEvent).order_by(SiteEvent.created_at.desc())
        ).all()
        conversations = self.session.scalars(
            select(AssistantConversation)
            .options(selectinload(AssistantConversation.messages))
            .order_by(AssistantConversation.last_message_at.desc())
        ).all()

        visitors, visits = self._build_site_activity_rollups(events)
        conversation_links = self._build_conversation_activity_links(events)

        return AdminSiteActivityOut(
            summary=AdminSiteActivitySummaryOut(
                total_events=len(events),
                unique_visitors=len({event.visitor_id for event in events if event.visitor_id}),
                page_views=sum(1 for event in events if event.event_type == EventType.PAGE_VIEW),
                assistant_messages=sum(1 for event in events if event.event_type == EventType.ASSISTANT_MESSAGE),
                contact_submissions=sum(1 for event in events if event.event_type == EventType.CONTACT_SUBMIT),
            ),
            visitors=visitors,
            visits=visits,
            events=[self._map_site_event(item) for item in events],
            assistant_conversations=[
                self._map_assistant_conversation(item, conversation_links.get(str(item.id))) for item in conversations
            ],
        )

    def update_contact_message_status(self, message_id: UUID, *, is_read: bool) -> AdminContactMessageOut | None:
        message = self.session.get(ContactMessage, message_id)
        if message is None:
            return None
        message.is_read = is_read
        self.session.commit()
        self.session.refresh(message)
        return self._map_contact_message(message)
