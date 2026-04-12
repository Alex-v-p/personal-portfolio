from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.db.models import EventType
from app.repositories.contact_message_repository import ContactMessageRepository
from app.schemas.contact import ContactMessageCreatedOut, ContactMessageIn
from app.services.site_event_service import SiteEventService

router = APIRouter()


@router.post('/messages', response_model=ContactMessageCreatedOut, status_code=status.HTTP_201_CREATED)
def create_contact_message(
    payload: ContactMessageIn,
    request: Request,
    session: Session = Depends(get_session),
) -> ContactMessageCreatedOut:
    repository = ContactMessageRepository(session)
    saved_item = repository.create(payload)
    SiteEventService(session).record_event(
        event_type=EventType.CONTACT_SUBMIT,
        page_path=payload.source_page,
        visitor_id=payload.visitor_id,
        session_id=payload.session_id,
        request=request,
        metadata={
            'contact_message_id': saved_item.id,
            'subject': saved_item.subject,
        },
    )
    session.commit()
    return ContactMessageCreatedOut(
        message='Contact message saved.',
        item=saved_item,
    )
