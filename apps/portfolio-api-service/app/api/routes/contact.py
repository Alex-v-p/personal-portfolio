from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import EventType
from app.db.session import get_session
from app.repositories.contact_message_repository import ContactMessageRepository
from app.schemas.contact import ContactMessageCreatedOut, ContactMessageIn
from app.services.request_protection import derive_request_identifier, enforce_rate_limit_or_429, ensure_payload_size_within_limit
from app.services.site_event_service import SiteEventService

router = APIRouter()


@router.post('/messages', response_model=ContactMessageCreatedOut, status_code=status.HTTP_201_CREATED)
def create_contact_message(
    payload: ContactMessageIn,
    request: Request,
    session: Session = Depends(get_session),
) -> ContactMessageCreatedOut:
    settings = get_settings()
    ensure_payload_size_within_limit(
        payload,
        max_bytes=settings.contact_max_request_bytes,
        detail='Contact message payload is too large.',
    )
    if payload.website and payload.website.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Spam protection triggered.')
    enforce_rate_limit_or_429(
        scope='contact-submit',
        identifier=derive_request_identifier(request, payload.visitor_id, payload.session_id),
        limit=settings.contact_rate_limit_max_requests,
        window_seconds=settings.contact_rate_limit_window_seconds,
        detail='Too many contact form submissions. Please try again later.',
    )

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
