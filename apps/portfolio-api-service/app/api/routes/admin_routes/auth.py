from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.repositories.admin.users import AdminUsersRepository
from app.schemas.admin import AdminAuthTokenOut, AdminLoginIn, AdminUserOut
from app.services.admin.auth_service import AdminAuthService

router = APIRouter()


@router.post('/auth/login', response_model=AdminAuthTokenOut)
def login(payload: AdminLoginIn, session: SessionDep) -> AdminAuthTokenOut:
    return AdminAuthService(session).login(payload)


@router.get('/auth/me', response_model=AdminUserOut)
def get_me(current_admin: CurrentAdminDep, session: SessionDep) -> AdminUserOut:
    return AdminUsersRepository(session).map_admin_user(current_admin)
