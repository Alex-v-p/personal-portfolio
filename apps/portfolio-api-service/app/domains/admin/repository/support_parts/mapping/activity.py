from __future__ import annotations

from app.db.models import SiteEvent
from app.domains.admin.schema import AdminSiteEventOut


class AdminRepositoryActivityMappingMixin:
    def _map_site_event(self, event: SiteEvent, *, retention_seconds: int, now=None) -> AdminSiteEventOut:
        metadata = event.metadata_json or None
        ip_address = None

        if isinstance(metadata, dict):
            ip_value = metadata.get('ip_address')
            if isinstance(ip_value, str):
                ip_address = ip_value

        retention_ends_at, seconds_until_retention_end = self._future_deadline(
            event.created_at,
            seconds=retention_seconds,
            now=now,
        )

        return AdminSiteEventOut(
            id=str(event.id),
            event_type=event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            page_path=event.page_path,
            visitor_id=event.visitor_id,
            session_id=event.session_id,
            referrer=event.referrer,
            user_agent=event.user_agent,
            ip_address=ip_address,
            metadata=metadata,
            created_at=self._serialize_datetime(event.created_at),
            retention_ends_at=retention_ends_at,
            seconds_until_retention_end=seconds_until_retention_end,
        )
