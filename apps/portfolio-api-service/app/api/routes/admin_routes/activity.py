from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.repositories.admin.activity import AdminActivityRepository
from app.schemas.admin import AdminContactMessageOut, AdminContactMessagesListOut, AdminMessageStatusUpdateIn, AdminSiteActivityOut

router = APIRouter()


def repository(session: SessionDep) -> AdminActivityRepository:
    return AdminActivityRepository(session)


@router.get('/site-activity', response_model=AdminSiteActivityOut)
def get_site_activity(_: CurrentAdminDep, session: SessionDep) -> AdminSiteActivityOut:
    return repository(session).get_site_activity()


@router.get('/contact-messages', response_model=AdminContactMessagesListOut)
def list_contact_messages(_: CurrentAdminDep, session: SessionDep) -> AdminContactMessagesListOut:
    items = repository(session).list_contact_messages()
    return AdminContactMessagesListOut(items=items, total=len(items))


@router.patch('/contact-messages/{message_id}', response_model=AdminContactMessageOut)
def update_contact_message(message_id: UUID, payload: AdminMessageStatusUpdateIn, _: CurrentAdminDep, session: SessionDep) -> AdminContactMessageOut:
    message = repository(session).update_contact_message_status(message_id, is_read=payload.is_read)
    if message is None:
        raise HTTPException(status_code=404, detail='Contact message not found.')
    return message
