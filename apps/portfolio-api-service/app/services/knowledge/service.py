from __future__ import annotations

from collections import Counter
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models import KnowledgeChunk, KnowledgeDocument
from app.services.knowledge.chunking import chunk_markdown
from app.services.knowledge.documents import KnowledgeDocumentBuilder
from app.services.knowledge.embedding import KnowledgeEmbeddingClient
from app.services.knowledge.models import KnowledgeSyncReport


class KnowledgeSyncService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.embedding_client = KnowledgeEmbeddingClient()
        self.document_builder = KnowledgeDocumentBuilder(session)

    def rebuild(self) -> KnowledgeSyncReport:
        self.session.execute(delete(KnowledgeChunk))
        self.session.execute(delete(KnowledgeDocument))
        self.session.flush()

        documents = self.document_builder.build_documents()
        for document in documents:
            self.session.add(document)
            self.session.flush()
            for index, chunk_text in enumerate(chunk_markdown(document.content_markdown)):
                self.session.add(
                    KnowledgeChunk(
                        id=uuid4(),
                        document_id=document.id,
                        chunk_index=index,
                        chunk_text=chunk_text,
                        embedding_vector=self.embedding_client.embed(chunk_text),
                        metadata_json={'source_type': document.source_type.value, **(document.metadata_json or {})},
                    )
                )

        self.session.commit()
        return self.get_status()

    def get_status(self) -> KnowledgeSyncReport:
        documents = self.session.scalars(select(KnowledgeDocument).order_by(KnowledgeDocument.updated_at.desc())).all()
        chunks = self.session.scalars(select(KnowledgeChunk)).all()
        by_source = Counter(
            document.source_type.value if hasattr(document.source_type, 'value') else str(document.source_type)
            for document in documents
        )
        latest_updated_at = documents[0].updated_at.isoformat() if documents else None
        return KnowledgeSyncReport(
            total_documents=len(documents),
            total_chunks=len(chunks),
            documents_by_source_type=dict(sorted(by_source.items())),
            latest_updated_at=latest_updated_at,
        )
