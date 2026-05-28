from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import AdminContactMessageOut, AdminContactMessagesListOut, AdminMessageStatusUpdateIn, AdminSiteActivityOut
from app.domains.admin.service.admin_activity_service import AdminActivityService

router = APIRouter()


@router.get('/site-activity', response_model=AdminSiteActivityOut)
def get_site_activity(_: CurrentAdminDep, session: SessionDep) -> AdminSiteActivityOut:
    return AdminActivityService(session).get_site_activity()


@router.get('/contact-messages', response_model=AdminContactMessagesListOut)
def list_contact_messages(_: CurrentAdminDep, session: SessionDep) -> AdminContactMessagesListOut:
    return AdminActivityService(session).list_contact_messages()


@router.patch('/contact-messages/{message_id}', response_model=AdminContactMessageOut)
def update_contact_message(message_id: UUID, payload: AdminMessageStatusUpdateIn, _: CurrentAdminDep, session: SessionDep) -> AdminContactMessageOut:
    return AdminActivityService(session).update_contact_message_status(message_id, is_read=payload.is_read)
