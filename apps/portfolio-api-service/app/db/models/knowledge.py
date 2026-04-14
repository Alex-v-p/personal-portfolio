from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import Enum as SqlEnum, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import KnowledgeSourceType
from app.db.types import Vector


class KnowledgeDocument(TimestampMixin, Base):
    __tablename__ = 'knowledge_documents'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    source_type: Mapped[KnowledgeSourceType] = mapped_column(SqlEnum(KnowledgeSourceType, native_enum=False), nullable=False)
    source_id: Mapped[UUID | None] = mapped_column(Uuid)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    canonical_url: Mapped[str | None] = mapped_column(String(500))
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    content_platform: Mapped[str | None] = mapped_column(String(120))
    metadata_json: Mapped[dict] = mapped_column('metadata', JSON, nullable=False, default=dict)

    chunks: Mapped[list['KnowledgeChunk']] = relationship(
        back_populates='document', cascade='all, delete-orphan'
    )


class KnowledgeChunk(Base):
    __tablename__ = 'knowledge_chunks'
    __table_args__ = (
        UniqueConstraint('document_id', 'chunk_index', name='uq_knowledge_chunks_document_chunk_index'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    document_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('knowledge_documents.id', ondelete='CASCADE'), nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_vector: Mapped[str | None] = mapped_column(Vector())
    metadata_json: Mapped[dict | None] = mapped_column('metadata', JSON)

    document: Mapped[KnowledgeDocument] = relationship(back_populates='chunks')
