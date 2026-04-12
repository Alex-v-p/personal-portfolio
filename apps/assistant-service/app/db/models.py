from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, JSON, String, Text, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AssistantRole(str, Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class KnowledgeSourceType(str, Enum):
    PROFILE = 'profile'
    PROJECT = 'project'
    BLOG_POST = 'blog_post'
    EXPERIENCE = 'experience'


class AssistantConversation(Base):
    __tablename__ = 'assistant_conversations'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    session_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_message_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    messages: Mapped[list['AssistantMessage']] = relationship(back_populates='conversation', cascade='all, delete-orphan')


class AssistantMessage(Base):
    __tablename__ = 'assistant_messages'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    conversation_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('assistant_conversations.id', ondelete='CASCADE'), nullable=False)
    role: Mapped[AssistantRole] = mapped_column(SqlEnum(AssistantRole, native_enum=False), nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    conversation: Mapped[AssistantConversation] = relationship(back_populates='messages')


class KnowledgeDocument(Base):
    __tablename__ = 'knowledge_documents'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    source_type: Mapped[KnowledgeSourceType] = mapped_column(SqlEnum(KnowledgeSourceType, native_enum=False), nullable=False)
    source_id: Mapped[UUID | None] = mapped_column(Uuid)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    canonical_url: Mapped[str | None] = mapped_column(String(500))
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    content_platform: Mapped[str | None] = mapped_column(String(120))
    metadata_json: Mapped[dict] = mapped_column('metadata', JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    chunks: Mapped[list['KnowledgeChunk']] = relationship(back_populates='document')


class KnowledgeChunk(Base):
    __tablename__ = 'knowledge_chunks'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    document_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('knowledge_documents.id', ondelete='CASCADE'), nullable=False)
    chunk_index: Mapped[int]
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_vector: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict | None] = mapped_column('metadata', JSON)

    document: Mapped[KnowledgeDocument] = relationship(back_populates='chunks')
