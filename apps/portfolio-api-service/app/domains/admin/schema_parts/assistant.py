from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.schemas.base import ApiSchema

TranslationLocaleLiteral = Literal['en', 'nl']


class AdminAssistantKnowledgeStatusOut(ApiSchema):
    total_documents: int
    total_chunks: int
    documents_by_source_type: dict[str, int]
    latest_updated_at: str | None = None


class AdminAssistantKnowledgeRebuildIn(ApiSchema):
    pass


class AdminAssistantKnowledgeRebuildOut(AdminAssistantKnowledgeStatusOut):
    pass


class AdminTranslationDraftIn(ApiSchema):
    source_locale: TranslationLocaleLiteral = 'en'
    target_locale: TranslationLocaleLiteral = 'nl'
    entity_type: str = Field(min_length=1, max_length=120)
    fields: dict[str, str] = Field(default_factory=dict)
    context: str | None = None


class AdminTranslationDraftOut(ApiSchema):
    source_locale: TranslationLocaleLiteral
    target_locale: TranslationLocaleLiteral
    entity_type: str
    translated_fields: dict[str, str] = Field(default_factory=dict)
    provider_backend: str
    provider_model: str | None = None
    warnings: list[str] = Field(default_factory=list)


__all__ = [
    'AdminAssistantKnowledgeRebuildIn',
    'AdminAssistantKnowledgeRebuildOut',
    'AdminAssistantKnowledgeStatusOut',
    'AdminTranslationDraftIn',
    'AdminTranslationDraftOut',
    'TranslationLocaleLiteral',
]
