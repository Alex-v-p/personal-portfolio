from __future__ import annotations

import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class ProviderClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate_answer(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None = None,
    ) -> str | None:
        backend = self.settings.provider_backend.strip().lower()
        if backend == 'mock':
            logger.info('Assistant provider backend is mock; skipping text generation.')
            return None
        if backend == 'ollama':
            return self._generate_with_ollama(question=question, context_blocks=context_blocks, history=history, page_path=page_path)
        if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
            return self._generate_with_openai_compatible(question=question, context_blocks=context_blocks, history=history, page_path=page_path)
        logger.warning('Unknown assistant provider backend: %s', backend)
        return None

    def _generate_with_ollama(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None,
    ) -> str | None:
        messages = self._build_messages(question=question, context_blocks=context_blocks, history=history, page_path=page_path)
        payload = self._post_json_with_retries(
            f"{self.settings.provider_base_url.rstrip('/')}/api/chat",
            json={
                'model': self.settings.provider_model,
                'stream': False,
                'messages': messages,
                'options': {'temperature': 0.25},
            },
        )
        message = (payload.get('message') or {}).get('content')
        if isinstance(message, str) and message.strip():
            return message.strip()
        return None

    def _generate_with_openai_compatible(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None,
    ) -> str | None:
        headers = {'Content-Type': 'application/json'}
        if self.settings.provider_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.provider_api_key.strip()}"
        messages = self._build_messages(question=question, context_blocks=context_blocks, history=history, page_path=page_path)
        payload = self._post_json_with_retries(
            f"{self.settings.provider_base_url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json={
                'model': self.settings.provider_model,
                'messages': messages,
                'temperature': 0.2,
            },
        )
        choices = payload.get('choices') or []
        if not choices:
            return None
        message = (choices[0].get('message') or {}).get('content')
        return message.strip() if isinstance(message, str) and message.strip() else None

    def _build_messages(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None,
    ) -> list[dict[str, str]]:
        context = '\n\n'.join(context_blocks) if context_blocks else 'No indexed portfolio context was found.'
        current_page = page_path or 'unknown'
        system_prompt = (
            'You are the assistant embedded on a developer portfolio website. '
            'You are helping a visitor evaluate the portfolio, usually someone like a recruiter, hiring manager, collaborator, or client. '
            'Do not talk as if you are the portfolio owner. Refer to the owner in the third person as "the developer", '
            '"the portfolio owner", or by name only if the context clearly contains it. '
            'Answer naturally and concisely, like a helpful guide on the site. '
            'Use the retrieved context selectively: decide which pieces are actually relevant to the question and ignore off-topic chunks, even if they were retrieved. '
            'For project questions, prioritize projects first and use profile or introduction details only as supporting background. '
            'For experience questions, prioritize experience entries. For blog questions, prioritize blog posts. '
            'Never dump raw retrieved chunks, never say "indexed matches", and never list irrelevant sections just because they were provided. '
            'If the context is weak or does not support the answer, say so briefly and offer the closest helpful answer instead.'
        )
        messages: list[dict[str, str]] = [{'role': 'system', 'content': system_prompt}]
        for item in history[-6:]:
            if item['role'] in {'user', 'assistant'}:
                messages.append({'role': item['role'], 'content': item['text']})
        messages.append(
            {
                'role': 'user',
                'content': (
                    f'Current page: {current_page}\n\n'
                    'Retrieved portfolio context:\n'
                    f'{context}\n\n'
                    'Visitor question:\n'
                    f'{question}\n\n'
                    'Write a direct answer for the visitor. Synthesize only the relevant context, '
                    'mention concrete examples when helpful, and avoid quoting or enumerating unrelated sections.'
                ),
            }
        )
        return messages


    def check_health(self) -> tuple[bool, str]:
        backend = self.settings.provider_backend.strip().lower()
        if backend == 'mock':
            return True, 'Preview mode is enabled. Responses use the local fallback formatter instead of a live model.'
        if backend == 'ollama':
            return self._check_ollama_health()
        if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
            return self._check_openai_compatible_health()
        return False, f'Unknown assistant provider backend: {self.settings.provider_backend}.'

    def _check_ollama_health(self) -> tuple[bool, str]:
        timeout_seconds = min(max(self.settings.provider_request_timeout_seconds, 1.0), 3.0)
        try:
            with httpx.Client(timeout=timeout_seconds) as client:
                response = client.get(f"{self.settings.provider_base_url.rstrip('/')}/api/tags")
                response.raise_for_status()
                payload = response.json()
            models = payload.get('models') if isinstance(payload, dict) else []
            if isinstance(models, list):
                available_models = [
                    item.get('name')
                    for item in models
                    if isinstance(item, dict) and isinstance(item.get('name'), str)
                ]
                if self.settings.provider_model in available_models:
                    return True, f'Ollama is online and model {self.settings.provider_model} is available.'
                if available_models:
                    return True, f'Ollama is online. Using configured model {self.settings.provider_model} if it is pulled locally.'
            return True, 'Ollama is online.'
        except httpx.TimeoutException:
            return False, 'Timed out while checking the Ollama instance.'
        except httpx.NetworkError:
            return False, 'Could not reach the Ollama instance.'
        except httpx.HTTPStatusError as exc:
            return False, f'Ollama returned HTTP {exc.response.status_code} during the availability check.'
        except Exception:
            logger.exception('Assistant provider health check failed for Ollama.')
            return False, 'The Ollama availability check failed unexpectedly.'

    def _check_openai_compatible_health(self) -> tuple[bool, str]:
        timeout_seconds = min(max(self.settings.provider_request_timeout_seconds, 1.0), 3.0)
        headers = {'Content-Type': 'application/json'}
        if self.settings.provider_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.provider_api_key.strip()}"
        try:
            with httpx.Client(timeout=timeout_seconds) as client:
                response = client.get(f"{self.settings.provider_base_url.rstrip('/')}/v1/models", headers=headers)
                response.raise_for_status()
            return True, 'The configured assistant model endpoint is reachable.'
        except httpx.TimeoutException:
            return False, 'Timed out while checking the configured model endpoint.'
        except httpx.NetworkError:
            return False, 'Could not reach the configured model endpoint.'
        except httpx.HTTPStatusError as exc:
            return False, f'The configured model endpoint returned HTTP {exc.response.status_code}.'
        except Exception:
            logger.exception('Assistant provider health check failed for OpenAI-compatible backend.')
            return False, 'The configured model endpoint health check failed unexpectedly.'

    def _post_json_with_retries(self, url: str, **kwargs) -> dict:
        max_attempts = max(self.settings.provider_max_retries, 0) + 1
        last_error: Exception | None = None
        for attempt in range(1, max_attempts + 1):
            try:
                with httpx.Client(timeout=self.settings.provider_request_timeout_seconds) as client:
                    response = client.post(url, **kwargs)
                    response.raise_for_status()
                    return response.json()
            except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as exc:
                last_error = exc
                if not self._should_retry(exc=exc, attempt=attempt, max_attempts=max_attempts):
                    raise
                logger.warning('Assistant provider call failed on attempt %s/%s: %s', attempt, max_attempts, exc)
        if last_error is not None:
            raise last_error
        return {}

    def _should_retry(self, *, exc: Exception, attempt: int, max_attempts: int) -> bool:
        if attempt >= max_attempts:
            return False
        if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
            return True
        if isinstance(exc, httpx.HTTPStatusError):
            status_code = exc.response.status_code
            return status_code in {408, 429, 500, 502, 503, 504}
        return False
