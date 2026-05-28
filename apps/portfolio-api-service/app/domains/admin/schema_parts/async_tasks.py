from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from app.schemas.base import ApiSchema

AdminAsyncTaskStatusLiteral = Literal['queued', 'running', 'succeeded', 'failed']
AdminAsyncTaskTypeLiteral = Literal['github-refresh', 'assistant-knowledge-rebuild']


class AdminAsyncTaskAcceptedOut(ApiSchema):
    task_id: str
    task_type: AdminAsyncTaskTypeLiteral
    status: AdminAsyncTaskStatusLiteral
    poll_after_ms: int = Field(default=1200)


class AdminAsyncTaskStatusOut(ApiSchema):
    task_id: str
    task_type: AdminAsyncTaskTypeLiteral
    status: AdminAsyncTaskStatusLiteral
    submitted_at: str
    started_at: str | None = None
    completed_at: str | None = None
    error_message: str | None = None
    result: dict[str, Any] | None = None


__all__ = [
    'AdminAsyncTaskAcceptedOut',
    'AdminAsyncTaskStatusLiteral',
    'AdminAsyncTaskStatusOut',
    'AdminAsyncTaskTypeLiteral',
]
