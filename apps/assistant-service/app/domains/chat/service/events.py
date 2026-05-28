from __future__ import annotations

from typing import Any

from fastapi import Request

from app.db.models import EventType, SiteEvent


def record_assistant_site_event(
    session,
    *,
    visitor_id: str | None,
    site_session_id: str | None,
    page_path: str | None,
    request: Request | None,
    conversation_id: str,
    provider_backend: str,
    citations,
    question: str,
    answer: str,
    used_fallback: bool,
    assistant_session_id: str,
) -> None:
    metadata: dict[str, Any] = {
        'conversation_id': conversation_id,
        'provider_backend': provider_backend,
        'citation_count': len(citations),
        'used_fallback': used_fallback,
        'question_preview': question[:280],
        'answer_preview': answer[:280],
        'assistant_session_id': assistant_session_id,
    }
    client_ip = extract_client_ip(request)
    if client_ip:
        metadata['ip_address'] = client_ip
    user_agent = request.headers.get('user-agent')[:500] if request and request.headers.get('user-agent') else None
    referrer = request.headers.get('referer')[:500] if request and request.headers.get('referer') else None
    session.add(
        SiteEvent(
            visitor_id=(visitor_id or site_session_id or assistant_session_id or 'anonymous')[:255],
            session_id=site_session_id[:255] if site_session_id else None,
            page_path=(page_path or '/assistant')[:255],
            event_type=EventType.ASSISTANT_MESSAGE,
            referrer=referrer,
            user_agent=user_agent,
            metadata_json=metadata,
        )
    )


def extract_client_ip(request: Request | None) -> str | None:
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
