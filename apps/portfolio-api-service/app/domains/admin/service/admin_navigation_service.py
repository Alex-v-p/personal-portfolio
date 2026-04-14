from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.admin.repository.content import AdminContentManagementRepository
from app.domains.admin.schema import AdminNavigationItemOut, AdminNavigationItemsListOut, AdminNavigationItemUpsertIn


class AdminNavigationService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminContentManagementRepository(session)

    def list_navigation_items(self) -> AdminNavigationItemsListOut:
        items = self.repository.list_navigation_items()
        return AdminNavigationItemsListOut(items=items, total=len(items))

    def create_navigation_item(self, payload: AdminNavigationItemUpsertIn) -> AdminNavigationItemOut:
        return self.repository.create_navigation_item(payload)

    def update_navigation_item(self, item_id: UUID, payload: AdminNavigationItemUpsertIn) -> AdminNavigationItemOut:
        item = self.repository.update_navigation_item(item_id, payload)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Navigation item not found.')
        return item

    def delete_navigation_item(self, item_id: UUID) -> None:
        deleted = self.repository.delete_navigation_item(item_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Navigation item not found.')
