from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Iterable

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.db.models import KnowledgeChunk, KnowledgeDocument

_STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'to', 'for', 'of', 'in', 'on', 'with', 'is', 'are', 'be', 'as', 'at',
    'by', 'it', 'this', 'that', 'from', 'about', 'can', 'you', 'your', 'what', 'which', 'who', 'when',
    'where', 'how', 'i', 'me', 'my', 'we', 'our', 'us', 'do', 'does', 'did', 'tell', 'show', 'have', 'has',
    'please', 'would', 'could', 'portfolio', 'assistant'
}


@dataclass(slots=True)
class RetrievedChunk:
    title: str
    source_type: str
    canonical_url: str | None
    excerpt: str
    score: float


class RetrievalEmbeddingClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._disabled_reason: str | None = None

    @property
    def is_enabled(self) -> bool:
        return self.settings.retrieval_embedding_backend.strip().lower() not in {'', 'none', 'disabled'} and self._disabled_reason is None

    def embed(self, text: str) -> list[float] | None:
        if not text.strip() or not self.is_enabled:
            return None

        backend = self.settings.retrieval_embedding_backend.strip().lower()
        try:
            if backend == 'ollama':
                return self._embed_with_ollama(text)
            if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
                return self._embed_with_openai_compatible(text)
            self._disabled_reason = f'Unsupported embedding backend: {backend}'
            return None
        except Exception:  # pragma: no cover - graceful degradation when embedding provider is unavailable
            self._disabled_reason = 'embedding provider unavailable'
            return None

    def _embed_with_ollama(self, text: str) -> list[float] | None:
        with httpx.Client(timeout=self.settings.retrieval_embedding_timeout_seconds) as client:
            response = client.post(
                f"{self.settings.retrieval_embedding_base_url.rstrip('/')}/api/embed",
                json={
                    'model': self.settings.retrieval_embedding_model,
                    'input': text,
                },
            )
            response.raise_for_status()
            payload = response.json()
        embeddings = payload.get('embeddings') or []
        if embeddings and isinstance(embeddings[0], list):
            return self._normalize([float(value) for value in embeddings[0]])
        embedding = payload.get('embedding') or []
        if not embedding:
            return None
        return self._normalize([float(value) for value in embedding])

    def _embed_with_openai_compatible(self, text: str) -> list[float] | None:
        headers = {'Content-Type': 'application/json'}
        if self.settings.retrieval_embedding_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.retrieval_embedding_api_key.strip()}"
        with httpx.Client(timeout=self.settings.retrieval_embedding_timeout_seconds) as client:
            response = client.post(
                f"{self.settings.retrieval_embedding_base_url.rstrip('/')}/v1/embeddings",
                headers=headers,
                json={
                    'model': self.settings.retrieval_embedding_model,
                    'input': text,
                },
            )
            response.raise_for_status()
            payload = response.json()
        data = payload.get('data') or []
        if not data:
            return None
        embedding = data[0].get('embedding') or []
        if not embedding:
            return None
        return self._normalize([float(value) for value in embedding])

    def _normalize(self, vector: list[float]) -> list[float]:
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]


class KnowledgeRetrievalService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.settings = get_settings()
        self.embedding_client = RetrievalEmbeddingClient()

    def search(self, query: str) -> list[RetrievedChunk]:
        tokens = self._tokenize(query)
        query_vector = self.embedding_client.embed(query)
        if not tokens and query_vector is None:
            return []

        documents = self.session.scalars(
            select(KnowledgeDocument).options(selectinload(KnowledgeDocument.chunks))
        ).all()

        results: list[RetrievedChunk] = []
        for document in documents:
            for chunk in document.chunks:
                score = self._score(document=document, chunk=chunk, query=query, tokens=tokens, query_vector=query_vector)
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

    def _score(
        self,
        *,
        document: KnowledgeDocument,
        chunk: KnowledgeChunk,
        query: str,
        tokens: Iterable[str],
        query_vector: list[float] | None,
    ) -> float:
        chunk_text = (chunk.chunk_text or '').lower()
        title = (document.title or '').lower()
        metadata_text = self._metadata_text(document.metadata_json)
        phrase = query.strip().lower()

        lexical_score = 0.0
        matched_tokens = 0
        token_list = list(tokens)
        for token in token_list:
            chunk_hits = chunk_text.count(token)
            title_hits = title.count(token)
            metadata_hits = metadata_text.count(token)
            if chunk_hits or title_hits or metadata_hits:
                matched_tokens += 1
            lexical_score += min(chunk_hits, 4) * 1.8
            lexical_score += min(title_hits, 2) * 3.2
            lexical_score += min(metadata_hits, 3) * 1.4

        if token_list:
            lexical_score += (matched_tokens / len(token_list)) * 5.5
        if phrase and phrase in chunk_text:
            lexical_score += 7.0
        if phrase and phrase in title:
            lexical_score += 8.0
        if phrase and phrase in metadata_text:
            lexical_score += 3.0

        semantic_score = 0.0
        if query_vector is not None:
            chunk_vector = self._parse_vector(chunk.embedding_vector)
            if chunk_vector is not None and len(chunk_vector) == len(query_vector):
                semantic_score = max(self._dot(query_vector, chunk_vector), 0.0) * 18.0

        total = lexical_score + semantic_score
        if matched_tokens == 0 and semantic_score < 4.5:
            return 0.0
        return total

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

    def _excerpt(self, text: str, tokens: Iterable[str], limit: int = 300) -> str:
        plain = re.sub(r'\s+', ' ', text).strip()
        token_list = list(tokens)
        for token in token_list:
            idx = plain.lower().find(token)
            if idx >= 0:
                start = max(idx - 110, 0)
                end = min(idx + 210, len(plain))
                snippet = plain[start:end].strip()
                if start > 0:
                    snippet = f'…{snippet}'
                if end < len(plain):
                    snippet = f'{snippet}…'
                return snippet
        return plain[:limit] + ('…' if len(plain) > limit else '')

    def _parse_vector(self, value: object) -> list[float] | None:
        if value is None:
            return None
        if isinstance(value, list):
            return [float(item) for item in value]
        if isinstance(value, tuple):
            return [float(item) for item in value]
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            stripped = stripped.removeprefix('[').removesuffix(']')
            if not stripped:
                return None
            return [float(item.strip()) for item in stripped.split(',') if item.strip()]
        return None

    def _dot(self, left: list[float], right: list[float]) -> float:
        return sum(a * b for a, b in zip(left, right))
