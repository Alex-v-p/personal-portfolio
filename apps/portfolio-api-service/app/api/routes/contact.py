from __future__ import annotations

from fastapi import APIRouter, status

from app.schemas.contact import ContactMessageCreatedOut, ContactMessageIn
from app.services.contact_message_store import ContactMessageStore

router = APIRouter()
store = ContactMessageStore()


@router.post('/messages', response_model=ContactMessageCreatedOut, status_code=status.HTTP_201_CREATED)
def create_contact_message(payload: ContactMessageIn) -> ContactMessageCreatedOut:
    saved_item = store.save(payload)
    return ContactMessageCreatedOut(
        message='Contact message saved.',
        item=saved_item,
    )
