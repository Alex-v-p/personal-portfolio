from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import AdminNavigationItemOut, AdminNavigationItemsListOut, AdminNavigationItemUpsertIn
from app.domains.admin.service.admin_navigation_service import AdminNavigationService

router = APIRouter()


@router.get('/navigation-items', response_model=AdminNavigationItemsListOut)
def list_navigation_items(_: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemsListOut:
    return AdminNavigationService(session).list_navigation_items()


@router.post('/navigation-items', response_model=AdminNavigationItemOut, status_code=status.HTTP_201_CREATED)
def create_navigation_item(payload: AdminNavigationItemUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemOut:
    return AdminNavigationService(session).create_navigation_item(payload)


@router.put('/navigation-items/{item_id}', response_model=AdminNavigationItemOut)
def update_navigation_item(item_id: UUID, payload: AdminNavigationItemUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemOut:
    return AdminNavigationService(session).update_navigation_item(item_id, payload)


@router.delete('/navigation-items/{item_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_navigation_item(item_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    AdminNavigationService(session).delete_navigation_item(item_id)
