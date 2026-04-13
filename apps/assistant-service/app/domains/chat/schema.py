from __future__ import annotations

from pydantic import AliasChoices, Field

from app.schemas.base import ApiSchema


class CitationOut(ApiSchema):
    title: str
    source_type: str = Field(serialization_alias='sourceType')
    canonical_url: str | None = Field(default=None, serialization_alias='canonicalUrl')
    excerpt: str


class ChatMessageOut(ApiSchema):
    role: str
    text: str
    created_at: str | None = Field(default=None, serialization_alias='createdAt')
    citations: list[CitationOut] = Field(default_factory=list)


class ChatRequest(ApiSchema):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str | None = Field(default=None, max_length=255, validation_alias=AliasChoices('conversation_id', 'conversationId'))
    session_id: str | None = Field(default=None, max_length=255, validation_alias=AliasChoices('session_id', 'sessionId'))
    site_session_id: str | None = Field(default=None, max_length=255, validation_alias=AliasChoices('site_session_id', 'siteSessionId'))
    visitor_id: str | None = Field(default=None, max_length=255, validation_alias=AliasChoices('visitor_id', 'visitorId'))
    page_path: str | None = Field(default=None, max_length=255, validation_alias=AliasChoices('page_path', 'pagePath'))


class ChatResponse(ApiSchema):
    conversation_id: str = Field(serialization_alias='conversationId')
    message: str
    provider_backend: str = Field(serialization_alias='providerBackend')
    citations: list[CitationOut] = Field(default_factory=list)


class ConversationOut(ApiSchema):
    id: str
    session_id: str = Field(serialization_alias='sessionId')
    started_at: str = Field(serialization_alias='startedAt')
    last_message_at: str = Field(serialization_alias='lastMessageAt')
    messages: list[ChatMessageOut] = Field(default_factory=list)


class ConversationsListOut(ApiSchema):
    items: list[ConversationOut] = Field(default_factory=list)
    total: int = 0


class ProviderStatusOut(ApiSchema):
    backend: str
    model: str
    base_url: str | None = Field(default=None, serialization_alias='baseUrl')
    configured: bool


class KnowledgeStatusOut(ApiSchema):
    total_documents: int = Field(serialization_alias='totalDocuments')
    total_chunks: int = Field(serialization_alias='totalChunks')
    documents_by_source_type: dict[str, int] = Field(default_factory=dict, serialization_alias='documentsBySourceType')
    latest_updated_at: str | None = Field(default=None, serialization_alias='latestUpdatedAt')
