from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from app.db.models import NavigationItem
from app.domains.admin.schema import AdminNavigationItemOut, AdminNavigationItemUpsertIn


class AdminNavigationContentRepository:
    def list_navigation_items(self) -> list[AdminNavigationItemOut]:
        items = self.session.scalars(select(NavigationItem).order_by(NavigationItem.sort_order.asc(), NavigationItem.label.asc())).all()
        return [self._map_navigation_item(item) for item in items]

    def create_navigation_item(self, payload: AdminNavigationItemUpsertIn) -> AdminNavigationItemOut:
        item = NavigationItem(
            label=payload.label,
            label_nl=self._normalize_optional_text(payload.label_nl),
            route_path=payload.route_path,
            is_external=payload.is_external,
            sort_order=payload.sort_order,
            is_visible=payload.is_visible,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return self._map_navigation_item(item)

    def update_navigation_item(self, item_id: UUID, payload: AdminNavigationItemUpsertIn) -> AdminNavigationItemOut | None:
        item = self.session.get(NavigationItem, item_id)
        if item is None:
            return None
        item.label = payload.label
        item.label_nl = self._normalize_optional_text(payload.label_nl)
        item.route_path = payload.route_path
        item.is_external = payload.is_external
        item.sort_order = payload.sort_order
        item.is_visible = payload.is_visible
        self.session.commit()
        self.session.refresh(item)
        return self._map_navigation_item(item)

    def delete_navigation_item(self, item_id: UUID) -> bool:
        item = self.session.get(NavigationItem, item_id)
        if item is None:
            return False
        self.session.delete(item)
        self.session.commit()
        return True
