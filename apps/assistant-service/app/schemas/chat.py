from __future__ import annotations

from pydantic import Field

from app.schemas.base import ApiSchema


class CitationOut(ApiSchema):
    title: str
    source_type: str
    canonical_url: str | None = None
    excerpt: str


class ChatMessageOut(ApiSchema):
    role: str
    text: str
    created_at: str | None = None
    citations: list[CitationOut] = Field(default_factory=list)


class ChatRequest(ApiSchema):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str | None = None
    session_id: str | None = None
    page_path: str | None = None


class ChatResponse(ApiSchema):
    conversation_id: str
    message: str
    provider_backend: str
    citations: list[CitationOut] = Field(default_factory=list)


class ConversationOut(ApiSchema):
    id: str
    session_id: str
    started_at: str
    last_message_at: str
    messages: list[ChatMessageOut] = Field(default_factory=list)


class ConversationsListOut(ApiSchema):
    items: list[ConversationOut] = Field(default_factory=list)
    total: int = 0


class ProviderStatusOut(ApiSchema):
    backend: str
    model: str
    base_url: str | None = None
    configured: bool


class KnowledgeStatusOut(ApiSchema):
    total_documents: int
    total_chunks: int
    documents_by_source_type: dict[str, int] = Field(default_factory=dict)
    latest_updated_at: str | None = None
