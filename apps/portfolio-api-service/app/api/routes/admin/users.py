from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import AdminUserCreateIn, AdminUserOut, AdminUserUpdateIn
from app.domains.admin.service.admin_users_service import AdminUsersService

router = APIRouter()


@router.get('/admin-users', response_model=list[AdminUserOut])
def list_admin_users(_: CurrentAdminDep, session: SessionDep) -> list[AdminUserOut]:
    return AdminUsersService(session).list_admin_users()


@router.post('/admin-users', response_model=AdminUserOut, status_code=status.HTTP_201_CREATED)
def create_admin_user(payload: AdminUserCreateIn, _: CurrentAdminDep, session: SessionDep) -> AdminUserOut:
    return AdminUsersService(session).create_admin_user(payload)


@router.put('/admin-users/{admin_user_id}', response_model=AdminUserOut)
def update_admin_user(admin_user_id: UUID, payload: AdminUserUpdateIn, _: CurrentAdminDep, session: SessionDep) -> AdminUserOut:
    return AdminUsersService(session).update_admin_user(admin_user_id, payload)


@router.delete('/admin-users/{admin_user_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_admin_user(admin_user_id: UUID, current_admin: CurrentAdminDep, session: SessionDep) -> None:
    AdminUsersService(session).delete_admin_user(admin_user_id, current_admin_id=current_admin.id)
