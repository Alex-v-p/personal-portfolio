from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.api.routes.admin_routes.content_routes.common import repository
from app.schemas.admin import AdminNavigationItemOut, AdminNavigationItemsListOut, AdminNavigationItemUpsertIn

router = APIRouter()


@router.get('/navigation-items', response_model=AdminNavigationItemsListOut)
def list_navigation_items(_: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemsListOut:
    items = repository(session).list_navigation_items()
    return AdminNavigationItemsListOut(items=items, total=len(items))


@router.post('/navigation-items', response_model=AdminNavigationItemOut, status_code=status.HTTP_201_CREATED)
def create_navigation_item(payload: AdminNavigationItemUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemOut:
    return repository(session).create_navigation_item(payload)


@router.put('/navigation-items/{item_id}', response_model=AdminNavigationItemOut)
def update_navigation_item(item_id: UUID, payload: AdminNavigationItemUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemOut:
    item = repository(session).update_navigation_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail='Navigation item not found.')
    return item


@router.delete('/navigation-items/{item_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_navigation_item(item_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = repository(session).delete_navigation_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Navigation item not found.')
