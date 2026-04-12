from __future__ import annotations

import httpx

from app.core.config import get_settings


class ProviderClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate_answer(self, *, question: str, context_blocks: list[str], history: list[dict[str, str]]) -> str | None:
        backend = self.settings.provider_backend.strip().lower()
        if backend == 'mock':
            return None
        if backend == 'ollama':
            return self._generate_with_ollama(question=question, context_blocks=context_blocks, history=history)
        if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
            return self._generate_with_openai_compatible(question=question, context_blocks=context_blocks, history=history)
        return None

    def _generate_with_ollama(self, *, question: str, context_blocks: list[str], history: list[dict[str, str]]) -> str | None:
        messages = self._build_messages(question=question, context_blocks=context_blocks, history=history)
        with httpx.Client(timeout=25.0) as client:
            response = client.post(
                f"{self.settings.provider_base_url.rstrip('/')}/api/chat",
                json={
                    'model': self.settings.provider_model,
                    'stream': False,
                    'messages': messages,
                },
            )
            response.raise_for_status()
            payload = response.json()
        message = (payload.get('message') or {}).get('content')
        if isinstance(message, str) and message.strip():
            return message.strip()
        return None

    def _generate_with_openai_compatible(self, *, question: str, context_blocks: list[str], history: list[dict[str, str]]) -> str | None:
        headers = {'Content-Type': 'application/json'}
        if self.settings.provider_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.provider_api_key.strip()}"
        messages = self._build_messages(question=question, context_blocks=context_blocks, history=history)
        with httpx.Client(timeout=25.0) as client:
            response = client.post(
                f"{self.settings.provider_base_url.rstrip('/')}/v1/chat/completions",
                headers=headers,
                json={
                    'model': self.settings.provider_model,
                    'messages': messages,
                    'temperature': 0.2,
                },
            )
            response.raise_for_status()
            payload = response.json()
        choices = payload.get('choices') or []
        if not choices:
            return None
        message = (choices[0].get('message') or {}).get('content')
        return message.strip() if isinstance(message, str) and message.strip() else None

    def _build_messages(self, *, question: str, context_blocks: list[str], history: list[dict[str, str]]) -> list[dict[str, str]]:
        context = '\n\n'.join(context_blocks) if context_blocks else 'No indexed portfolio context was found.'
        system_prompt = (
            'You are a portfolio assistant. Answer only from the provided portfolio context and recent conversation. '
            'If the answer is not supported by the context, say that clearly. Keep the tone concise and helpful.'
        )
        messages: list[dict[str, str]] = [{'role': 'system', 'content': system_prompt}]
        for item in history[-6:]:
            if item['role'] in {'user', 'assistant'}:
                messages.append({'role': item['role'], 'content': item['text']})
        messages.append({'role': 'user', 'content': f'Context:\n{context}\n\nQuestion: {question}'})
        return messages
