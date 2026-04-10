from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.contact_message_repository import ContactMessageRepository
from app.schemas.contact import ContactMessageCreatedOut, ContactMessageIn

router = APIRouter()


@router.post('/messages', response_model=ContactMessageCreatedOut, status_code=status.HTTP_201_CREATED)
def create_contact_message(
    payload: ContactMessageIn,
    session: Session = Depends(get_session),
) -> ContactMessageCreatedOut:
    repository = ContactMessageRepository(session)
    saved_item = repository.create(payload)
    return ContactMessageCreatedOut(
        message='Contact message saved.',
        item=saved_item,
    )
