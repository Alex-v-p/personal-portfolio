from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.models import EventType
from app.db.session import get_session
from app.schemas.site_events import SiteEventCreateIn, SiteEventCreatedOut
from app.services.site_event_service import SiteEventService

router = APIRouter()


@router.post('', response_model=SiteEventCreatedOut, status_code=status.HTTP_201_CREATED)
def create_site_event(
    payload: SiteEventCreateIn,
    request: Request,
    session: Session = Depends(get_session),
) -> SiteEventCreatedOut:
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
        metadata=payload.metadata,
    )
    session.commit()
    return SiteEventCreatedOut(message='Site event stored.', event_id=str(item.id))
