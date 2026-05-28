from __future__ import annotations

from typing import Any

from fastapi import Request
from sqlalchemy.orm import Session

from app.db.models import EventType, SiteEvent


class SiteEventService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def record_event(
        self,
        *,
        event_type: EventType,
        page_path: str,
        visitor_id: str | None,
        session_id: str | None,
        request: Request | None = None,
        referrer: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> SiteEvent:
        details = dict(metadata or {})
        client_ip = self._extract_client_ip(request)
        if client_ip and 'ip_address' not in details:
            details['ip_address'] = client_ip

        user_agent = None
        request_referrer = referrer
        if request is not None:
            user_agent = request.headers.get('user-agent')
            request_referrer = request_referrer or request.headers.get('referer')

        item = SiteEvent(
            visitor_id=(visitor_id or session_id or 'anonymous')[:255],
            session_id=session_id[:255] if session_id else None,
            page_path=page_path[:255],
            event_type=event_type,
            referrer=request_referrer[:500] if request_referrer else None,
            user_agent=user_agent[:500] if user_agent else None,
            metadata_json=details or None,
        )
        self.session.add(item)
        self.session.flush()
        return item

    def _extract_client_ip(self, request: Request | None) -> str | None:
        if request is None:
            return None
        forwarded_for = request.headers.get('x-forwarded-for')
        if forwarded_for:
            first = forwarded_for.split(',')[0].strip()
            if first:
                return first
        real_ip = request.headers.get('x-real-ip')
        if real_ip:
            return real_ip.strip()
        client = getattr(request, 'client', None)
        return getattr(client, 'host', None)
