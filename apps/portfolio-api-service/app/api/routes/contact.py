from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.contact.schema import ContactMessageCreatedOut, ContactMessageIn
from app.domains.contact.service.contact_submission_service import ContactSubmissionService

router = APIRouter()


@router.post('/messages', response_model=ContactMessageCreatedOut, status_code=status.HTTP_201_CREATED)
def create_contact_message(
    payload: ContactMessageIn,
    request: Request,
    session: Session = Depends(get_session),
) -> ContactMessageCreatedOut:
    return ContactSubmissionService(session).submit(payload, request)
