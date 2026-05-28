from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.models import EventType
from app.db.session import get_session
from app.domains.site_activity.schema import SiteEventCreateIn, SiteEventCreatedOut
from app.services.request_protection import (
    derive_request_identifier,
    enforce_rate_limit_or_429,
    ensure_payload_size_within_limit,
    sanitize_event_metadata,
)
from app.domains.site_activity.service import SiteEventService

router = APIRouter()


@router.post('', response_model=SiteEventCreatedOut, status_code=status.HTTP_201_CREATED)
def create_site_event(
    payload: SiteEventCreateIn,
    request: Request,
    session: Session = Depends(get_session),
) -> SiteEventCreatedOut:
    from app.core.config import get_settings

    settings = get_settings()
    ensure_payload_size_within_limit(
        payload,
        max_bytes=settings.events_max_request_bytes,
        detail='Site event payload is too large.',
    )
    enforce_rate_limit_or_429(
        scope='site-event',
        identifier=derive_request_identifier(request, payload.visitor_id, payload.session_id),
        limit=settings.events_rate_limit_max_requests,
        window_seconds=settings.events_rate_limit_window_seconds,
        detail='Too many site events were submitted in a short period. Please slow down.',
    )

    try:
        event_type = EventType(payload.event_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail='Invalid event type.') from exc

    item = SiteEventService(session).record_event(
        event_type=event_type,
        page_path=payload.page_path,
        visitor_id=payload.visitor_id,
        session_id=payload.session_id,
        request=request,
        referrer=payload.referrer,
        metadata=sanitize_event_metadata(
            payload.metadata,
            max_entries=settings.events_metadata_max_entries,
            max_depth=settings.events_metadata_max_depth,
            max_list_items=settings.events_metadata_max_list_items,
            max_string_length=settings.events_metadata_max_string_length,
        ),
    )
    session.commit()
    return SiteEventCreatedOut(message='Site event stored.', event_id=str(item.id))
