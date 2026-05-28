from __future__ import annotations

import math

import httpx

from app.core.config import get_settings


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
