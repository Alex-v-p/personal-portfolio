from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import AdminProfileOut, AdminProfileUpdateIn
from app.domains.admin.service.admin_profile_service import AdminProfileService

router = APIRouter()


@router.get('/profile', response_model=AdminProfileOut)
def get_profile(_: CurrentAdminDep, session: SessionDep) -> AdminProfileOut:
    return AdminProfileService(session).get_profile()


@router.put('/profile', response_model=AdminProfileOut)
def update_profile(payload: AdminProfileUpdateIn, _: CurrentAdminDep, session: SessionDep) -> AdminProfileOut:
    return AdminProfileService(session).update_profile(payload)
