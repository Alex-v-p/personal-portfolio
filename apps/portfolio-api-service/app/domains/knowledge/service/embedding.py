from __future__ import annotations

import math

import httpx

from app.core.config import get_settings


class KnowledgeEmbeddingClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._disabled_reason: str | None = None

    @property
    def is_enabled(self) -> bool:
        return self.settings.knowledge_embedding_backend.strip().lower() not in {'', 'none', 'disabled'} and self._disabled_reason is None

    def embed(self, text: str) -> str | None:
        if not text.strip() or not self.is_enabled:
            return None

        backend = self.settings.knowledge_embedding_backend.strip().lower()
        try:
            if backend == 'ollama':
                vector = self._embed_with_ollama(text)
            elif backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
                vector = self._embed_with_openai_compatible(text)
            else:
                self._disabled_reason = f'Unsupported embedding backend: {backend}'
                return None
        except Exception as exc:  # pragma: no cover
            self._disabled_reason = str(exc)
            return None

        return self._format_vector(vector) if vector else None

    def _embed_with_ollama(self, text: str) -> list[float]:
        with httpx.Client(timeout=self.settings.knowledge_embedding_timeout_seconds) as client:
            response = client.post(
                f"{self.settings.knowledge_embedding_base_url.rstrip('/')}/api/embed",
                json={'model': self.settings.knowledge_embedding_model, 'input': text},
            )
            response.raise_for_status()
            payload = response.json()
        embeddings = payload.get('embeddings') or []
        if embeddings and isinstance(embeddings[0], list):
            return [float(value) for value in embeddings[0]]
        embedding = payload.get('embedding') or []
        return [float(value) for value in embedding]

    def _embed_with_openai_compatible(self, text: str) -> list[float]:
        headers = {'Content-Type': 'application/json'}
        if self.settings.knowledge_embedding_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.knowledge_embedding_api_key.strip()}"
        with httpx.Client(timeout=self.settings.knowledge_embedding_timeout_seconds) as client:
            response = client.post(
                f"{self.settings.knowledge_embedding_base_url.rstrip('/')}/v1/embeddings",
                headers=headers,
                json={'model': self.settings.knowledge_embedding_model, 'input': text},
            )
            response.raise_for_status()
            payload = response.json()
        data = payload.get('data') or []
        if not data:
            return []
        embedding = data[0].get('embedding') or []
        return [float(value) for value in embedding]

    @staticmethod
    def _format_vector(vector: list[float]) -> str:
        if not vector:
            return '[]'
        norm = math.sqrt(sum(value * value for value in vector))
        normalized = vector if norm == 0 else [value / norm for value in vector]
        return '[' + ','.join(f'{value:.8f}' for value in normalized) + ']'
