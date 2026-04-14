from __future__ import annotations

from typing import Any

from app.schemas.base import ApiSchema


class AdminContactMessageOut(ApiSchema):
    id: str
    name: str
    email: str
    subject: str
    message: str
    source_page: str
    is_read: bool
    created_at: str
    updated_at: str


class AdminContactMessagesListOut(ApiSchema):
    items: list[AdminContactMessageOut]
    total: int


class AdminMessageStatusUpdateIn(ApiSchema):
    is_read: bool


class AdminSiteEventOut(ApiSchema):
    id: str
    event_type: str
    page_path: str
    visitor_id: str
    session_id: str | None = None
    referrer: str | None = None
    user_agent: str | None = None
    ip_address: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: str
    retention_ends_at: str
    seconds_until_retention_end: int


class AdminVisitSessionSummaryOut(ApiSchema):
    session_id: str
    visitor_id: str
    started_at: str
    last_activity_at: str
    total_events: int
    page_views: int
    assistant_messages: int
    contact_submissions: int
    entry_page_path: str | None = None
    last_page_path: str | None = None
    ip_address: str | None = None
    retention_ends_at: str
    seconds_until_retention_end: int


class AdminVisitorActivitySummaryOut(ApiSchema):
    visitor_id: str
    first_seen_at: str
    last_seen_at: str
    total_events: int
    unique_sessions: int
    page_views: int
    assistant_messages: int
    contact_submissions: int
    latest_page_path: str | None = None
    latest_ip_address: str | None = None
    retention_ends_at: str
    seconds_until_retention_end: int


class AdminAssistantConversationSummaryOut(ApiSchema):
    id: str
    session_id: str
    visitor_id: str | None = None
    site_session_id: str | None = None
    page_path: str | None = None
    started_at: str
    last_message_at: str
    total_messages: int
    user_message_count: int
    assistant_message_count: int
    used_fallback: bool | None = None
    first_user_message: str | None = None
    latest_assistant_message: str | None = None
    retention_ends_at: str
    seconds_until_retention_end: int


class AdminSiteActivitySummaryOut(ApiSchema):
    total_events: int
    unique_visitors: int
    page_views: int
    assistant_messages: int
    contact_submissions: int
    site_events_retention_days: int
    assistant_activity_retention_days: int


class AdminSiteActivityOut(ApiSchema):
    summary: AdminSiteActivitySummaryOut
    visitors: list[AdminVisitorActivitySummaryOut]
    visits: list[AdminVisitSessionSummaryOut]
    events: list[AdminSiteEventOut]
    assistant_conversations: list[AdminAssistantConversationSummaryOut]


__all__ = [
    'AdminAssistantConversationSummaryOut',
    'AdminContactMessageOut',
    'AdminContactMessagesListOut',
    'AdminMessageStatusUpdateIn',
    'AdminSiteActivityOut',
    'AdminSiteActivitySummaryOut',
    'AdminSiteEventOut',
    'AdminVisitSessionSummaryOut',
    'AdminVisitorActivitySummaryOut',
]
