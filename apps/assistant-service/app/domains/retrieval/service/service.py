from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.db.models import KnowledgeChunk, KnowledgeDocument
from app.domains.retrieval.service.embedding import RetrievalEmbeddingClient
from app.domains.retrieval.service.intent import infer_intent
from app.domains.retrieval.service.ranking import build_retrieved_chunk, filter_ranked_results, score_chunk
from app.domains.retrieval.service.text import is_smalltalk, normalize_text, tokenize


class KnowledgeRetrievalService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.settings = get_settings()
        self.embedding_client = RetrievalEmbeddingClient()

    def search(self, query: str, *, page_path: str | None = None):
        normalized_query = normalize_text(query)
        if is_smalltalk(normalized_query):
            return []

        tokens = tokenize(query)
        query_vector = self.embedding_client.embed(query)
        if not tokens and query_vector is None:
            return []

        intent = infer_intent(query=query, page_path=page_path)
        documents = self.session.scalars(
            select(KnowledgeDocument).options(selectinload(KnowledgeDocument.chunks))
        ).all()

        scored = []
        for document in documents:
            source_type = document.source_type.value if hasattr(document.source_type, 'value') else str(document.source_type)
            for chunk in document.chunks:
                score = score_chunk(
                    document=document,
                    chunk=chunk,
                    query=query,
                    tokens=tokens,
                    query_vector=query_vector,
                    intent=intent,
                    page_path=page_path,
                    source_type=source_type,
                )
                if score <= 0:
                    continue
                scored.append(
                    build_retrieved_chunk(document=document, source_type=source_type, chunk=chunk, tokens=tokens, score=score)
                )

        scored.sort(key=lambda item: item.score, reverse=True)
        return filter_ranked_results(scored, intent, chunk_limit=self.settings.retrieval_chunk_limit)

    def get_status(self) -> dict:
        documents = self.session.scalars(select(KnowledgeDocument)).all()
        chunks = self.session.scalars(select(KnowledgeChunk)).all()
        total_documents = len(documents)
        by_source: dict[str, int] = {}
        latest_updated_at = None
        for document in documents:
            source_type = document.source_type.value if hasattr(document.source_type, 'value') else str(document.source_type)
            by_source[source_type] = by_source.get(source_type, 0) + 1
            if document.updated_at and (latest_updated_at is None or document.updated_at > latest_updated_at):
                latest_updated_at = document.updated_at
        return {
            'total_documents': total_documents,
            'total_chunks': len(chunks),
            'documents_by_source_type': by_source,
            'latest_updated_at': latest_updated_at.isoformat() if latest_updated_at else None,
        }
