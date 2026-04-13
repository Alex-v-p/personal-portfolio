from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.repositories.admin.users import AdminUsersRepository
from app.schemas.admin import AdminUserCreateIn, AdminUserOut, AdminUserUpdateIn

router = APIRouter()


def repository(session: SessionDep) -> AdminUsersRepository:
    return AdminUsersRepository(session)


@router.get('/admin-users', response_model=list[AdminUserOut])
def list_admin_users(_: CurrentAdminDep, session: SessionDep) -> list[AdminUserOut]:
    return repository(session).list_admin_users()


@router.post('/admin-users', response_model=AdminUserOut, status_code=status.HTTP_201_CREATED)
def create_admin_user(payload: AdminUserCreateIn, _: CurrentAdminDep, session: SessionDep) -> AdminUserOut:
    return repository(session).create_admin_user(payload)


@router.put('/admin-users/{admin_user_id}', response_model=AdminUserOut)
def update_admin_user(admin_user_id: UUID, payload: AdminUserUpdateIn, _: CurrentAdminDep, session: SessionDep) -> AdminUserOut:
    user = repository(session).update_admin_user(admin_user_id, payload)
    if user is None:
        raise HTTPException(status_code=404, detail='Admin user not found.')
    return user


@router.delete('/admin-users/{admin_user_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_admin_user(admin_user_id: UUID, current_admin: CurrentAdminDep, session: SessionDep) -> None:
    if current_admin.id == admin_user_id:
        raise HTTPException(status_code=400, detail='You cannot delete the currently signed-in admin user.')
    deleted = repository(session).delete_admin_user(admin_user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Admin user not found.')
