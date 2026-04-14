from __future__ import annotations

from app.db.models import NavigationItem
from app.domains.admin.schema import AdminNavigationItemOut


class AdminRepositoryNavigationMappingMixin:
    def _map_navigation_item(self, item: NavigationItem) -> AdminNavigationItemOut:
        return AdminNavigationItemOut(
            id=str(item.id),
            label=item.label,
            route_path=item.route_path,
            is_external=item.is_external,
            sort_order=item.sort_order,
            is_visible=item.is_visible,
        )
