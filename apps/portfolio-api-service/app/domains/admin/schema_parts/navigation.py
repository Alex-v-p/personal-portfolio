from __future__ import annotations

from pydantic import Field

from app.schemas.base import ApiSchema


class AdminNavigationItemUpsertIn(ApiSchema):
    label: str = Field(min_length=1, max_length=120)
    route_path: str = Field(min_length=1, max_length=255)
    is_external: bool = False
    sort_order: int = 0
    is_visible: bool = True


class AdminNavigationItemOut(ApiSchema):
    id: str
    label: str
    route_path: str
    is_external: bool
    sort_order: int
    is_visible: bool


class AdminNavigationItemsListOut(ApiSchema):
    items: list[AdminNavigationItemOut]
    total: int


__all__ = ['AdminNavigationItemOut', 'AdminNavigationItemsListOut', 'AdminNavigationItemUpsertIn']
