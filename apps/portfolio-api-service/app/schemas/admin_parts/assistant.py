from __future__ import annotations

from app.schemas.base import ApiSchema


class AdminAssistantKnowledgeStatusOut(ApiSchema):
    total_documents: int
    total_chunks: int
    documents_by_source_type: dict[str, int]
    latest_updated_at: str | None = None


class AdminAssistantKnowledgeRebuildIn(ApiSchema):
    pass


class AdminAssistantKnowledgeRebuildOut(AdminAssistantKnowledgeStatusOut):
    pass


__all__ = [
    'AdminAssistantKnowledgeRebuildIn',
    'AdminAssistantKnowledgeRebuildOut',
    'AdminAssistantKnowledgeStatusOut',
]
