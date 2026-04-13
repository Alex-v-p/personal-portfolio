from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.api.routes.admin_routes.content_routes.common import repository
from app.schemas.admin import AdminProfileOut, AdminProfileUpdateIn

router = APIRouter()


@router.get('/profile', response_model=AdminProfileOut)
def get_profile(_: CurrentAdminDep, session: SessionDep) -> AdminProfileOut:
    profile = repository(session).get_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail='Profile not found.')
    return profile


@router.put('/profile', response_model=AdminProfileOut)
def update_profile(payload: AdminProfileUpdateIn, _: CurrentAdminDep, session: SessionDep) -> AdminProfileOut:
    profile = repository(session).update_profile(payload)
    if profile is None:
        raise HTTPException(status_code=404, detail='Profile not found.')
    return profile
