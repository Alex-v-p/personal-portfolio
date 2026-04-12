from __future__ import annotations

from typing import Any

from pydantic import Field

from app.schemas.base import ApiSchema


class SiteEventCreateIn(ApiSchema):
    event_type: str = Field(min_length=1, max_length=80)
    page_path: str = Field(min_length=1, max_length=255)
    visitor_id: str | None = Field(default=None, max_length=255)
    session_id: str | None = Field(default=None, max_length=255)
    metadata: dict[str, Any] | None = None
    referrer: str | None = Field(default=None, max_length=500)


class SiteEventCreatedOut(ApiSchema):
    message: str
    event_id: str
