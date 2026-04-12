from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.db.models import KnowledgeChunk, KnowledgeDocument

_STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'to', 'for', 'of', 'in', 'on', 'with', 'is', 'are', 'be', 'as', 'at',
    'by', 'it', 'this', 'that', 'from', 'about', 'can', 'you', 'your', 'what', 'which', 'who', 'when',
    'where', 'how', 'i', 'me', 'my', 'we', 'our', 'us', 'do', 'does', 'did', 'tell', 'show', 'have', 'has'
}


@dataclass(slots=True)
class RetrievedChunk:
    title: str
    source_type: str
    canonical_url: str | None
    excerpt: str
    score: float


class KnowledgeRetrievalService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.settings = get_settings()

    def search(self, query: str) -> list[RetrievedChunk]:
        tokens = self._tokenize(query)
        if not tokens:
            return []

        documents = self.session.scalars(
            select(KnowledgeDocument).options(selectinload(KnowledgeDocument.chunks))
        ).all()

        results: list[RetrievedChunk] = []
        for document in documents:
            for chunk in document.chunks:
                score = self._score(document=document, chunk=chunk, query=query, tokens=tokens)
                if score <= 0:
                    continue
                results.append(
                    RetrievedChunk(
                        title=document.title,
                        source_type=document.source_type.value if hasattr(document.source_type, 'value') else str(document.source_type),
                        canonical_url=document.canonical_url,
                        excerpt=self._excerpt(chunk.chunk_text, tokens),
                        score=score,
                    )
                )

        results.sort(key=lambda item: item.score, reverse=True)
        deduped: list[RetrievedChunk] = []
        seen = set()
        for item in results:
            key = (item.title, item.excerpt)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)
            if len(deduped) >= self.settings.retrieval_chunk_limit:
                break
        return deduped

    def get_status(self) -> dict:
        documents = self.session.scalars(select(KnowledgeDocument)).all()
        total_documents = len(documents)
        chunks = self.session.scalars(select(KnowledgeChunk)).all()
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

    def _score(self, *, document: KnowledgeDocument, chunk: KnowledgeChunk, query: str, tokens: Iterable[str]) -> float:
        chunk_text = (chunk.chunk_text or '').lower()
        title = (document.title or '').lower()
        phrase = query.strip().lower()
        score = 0.0
        for token in tokens:
            score += chunk_text.count(token) * 1.6
            score += title.count(token) * 2.4
            metadata_text = self._metadata_text(document.metadata_json)
            score += metadata_text.count(token) * 0.9
        if phrase and phrase in chunk_text:
            score += 4.5
        if phrase and phrase in title:
            score += 5.0
        return score

    def _metadata_text(self, metadata: dict | None) -> str:
        if not metadata:
            return ''
        values: list[str] = []
        for value in metadata.values():
            if isinstance(value, str):
                values.append(value.lower())
            elif isinstance(value, list):
                values.extend(str(item).lower() for item in value)
        return ' '.join(values)

    def _tokenize(self, text: str) -> list[str]:
        return [token for token in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]{1,}", text.lower()) if token not in _STOP_WORDS]

    def _excerpt(self, text: str, tokens: Iterable[str], limit: int = 260) -> str:
        plain = re.sub(r'\s+', ' ', text).strip()
        for token in tokens:
            idx = plain.lower().find(token)
            if idx >= 0:
                start = max(idx - 80, 0)
                end = min(idx + 180, len(plain))
                snippet = plain[start:end].strip()
                if start > 0:
                    snippet = f'…{snippet}'
                if end < len(plain):
                    snippet = f'{snippet}…'
                return snippet
        return plain[:limit] + ('…' if len(plain) > limit else '')
