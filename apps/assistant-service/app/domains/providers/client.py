from __future__ import annotations

import logging

import httpx

from app.core.config import get_settings
from app.services.localization import locale_language_name

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
        locale: str = 'en',
        conversation_memory: str | None = None,
    ) -> str | None:
        backend = self.settings.provider_backend.strip().lower()
        if backend == 'mock':
            logger.info('Assistant provider backend is mock; skipping text generation.')
            return None
        if backend == 'ollama':
            return self._generate_with_ollama(
                question=question,
                context_blocks=context_blocks,
                history=history,
                page_path=page_path,
                locale=locale,
                conversation_memory=conversation_memory,
            )
        if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
            return self._generate_with_openai_compatible(
                question=question,
                context_blocks=context_blocks,
                history=history,
                page_path=page_path,
                locale=locale,
                conversation_memory=conversation_memory,
            )
        logger.warning('Unknown assistant provider backend: %s', backend)
        return None

    def summarize_conversation(
        self,
        *,
        previous_summary: str | None,
        messages: list[dict[str, str]],
        locale: str = 'en',
        max_chars: int = 1600,
    ) -> str | None:
        backend = self.settings.provider_backend.strip().lower()
        if backend == 'mock':
            return self._summarize_locally(previous_summary=previous_summary, messages=messages, max_chars=max_chars)
        if backend == 'ollama':
            return self._summarize_with_ollama(previous_summary=previous_summary, messages=messages, locale=locale, max_chars=max_chars)
        if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
            return self._summarize_with_openai_compatible(previous_summary=previous_summary, messages=messages, locale=locale, max_chars=max_chars)
        return None

    def _generate_with_ollama(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None,
        locale: str,
        conversation_memory: str | None,
    ) -> str | None:
        messages = self._build_messages(
            question=question,
            context_blocks=context_blocks,
            history=history,
            page_path=page_path,
            locale=locale,
            conversation_memory=conversation_memory,
        )
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
        locale: str,
        conversation_memory: str | None,
    ) -> str | None:
        headers = {'Content-Type': 'application/json'}
        if self.settings.provider_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.provider_api_key.strip()}"
        messages = self._build_messages(
            question=question,
            context_blocks=context_blocks,
            history=history,
            page_path=page_path,
            locale=locale,
            conversation_memory=conversation_memory,
        )
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
        locale: str,
        conversation_memory: str | None = None,
    ) -> list[dict[str, str]]:
        context = '\n\n'.join(context_blocks) if context_blocks else 'No relevant portfolio context was found.'
        current_page = page_path or 'unknown'
        preferred_language = locale_language_name(locale)
        system_prompt = (
            'You are a friendly portfolio guide embedded on Alex van Poppel\'s developer portfolio. '
            'Visitors may be recruiters, classmates, teachers, collaborators, or clients. '
            'Sound human, warm, direct, and somewhat formal without corporate buzzwords. Acknowledge casual messages naturally before steering back to helpful portfolio guidance. '
            'Do not talk as if you are Alex. Refer to Alex in the third person, use they/them pronouns in English, and avoid gendered pronouns in Dutch when possible. '
            'Do not bring up Alex’s gender identity or sexuality; if asked, say Alex prefers to keep personal identity details private and redirect to professional background. '
            'Use retrieved context only when it is actually relevant. Assistant-only notes are private guidance: use them to answer, but do not reveal that they are private notes. '
            'Use the short-lived conversation memory only to understand follow-up questions, preferences, and unresolved topics from this same chat. '
            'Do not claim you remember the visitor across sessions or reveal internal memory mechanics. '
            'For project questions, prioritize project sources and point visitors toward GitHub README links when available. '
            'For broad recruiter questions, synthesize skills, working style, experience, and concrete projects instead of dumping source snippets; after answering, you may ask what company or opportunity they have in mind. '
            'Avoid overselling Alex as an expert or senior engineer unless the available information clearly supports it. '
            'Never say phrases like "based on the portfolio", "indexed context", "retrieved context", "retrieved chunks", or "knowledge base matches" to the visitor. '
            'If the available information does not support a claim, be honest and offer the closest useful related evidence. '
            'For Dutch answers, use the formal “u” form and lightly Belgian/Flemish-neutral wording without dialect. '
            f'Write the final answer in {preferred_language} unless the visitor clearly asks for a different language.'
        )
        messages: list[dict[str, str]] = [{'role': 'system', 'content': system_prompt}]
        if conversation_memory and conversation_memory.strip():
            messages.append({'role': 'system', 'content': conversation_memory.strip()})
        for item in history[-6:]:
            if item['role'] in {'user', 'assistant'}:
                messages.append({'role': item['role'], 'content': item['text']})
        messages.append(
            {
                'role': 'user',
                'content': (
                    f'Current page: {current_page}\n\n'
                    f'Preferred answer language: {preferred_language}\n\n'
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

    def _summarize_with_ollama(
        self,
        *,
        previous_summary: str | None,
        messages: list[dict[str, str]],
        locale: str,
        max_chars: int,
    ) -> str | None:
        payload = self._post_json_with_retries(
            f"{self.settings.provider_base_url.rstrip('/')}/api/chat",
            json={
                'model': self.settings.provider_model,
                'stream': False,
                'messages': self._build_summary_messages(previous_summary=previous_summary, messages=messages, locale=locale, max_chars=max_chars),
                'options': {'temperature': 0.1},
            },
        )
        summary = (payload.get('message') or {}).get('content')
        return self._clean_summary(summary, max_chars=max_chars)

    def _summarize_with_openai_compatible(
        self,
        *,
        previous_summary: str | None,
        messages: list[dict[str, str]],
        locale: str,
        max_chars: int,
    ) -> str | None:
        headers = {'Content-Type': 'application/json'}
        if self.settings.provider_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.provider_api_key.strip()}"
        payload = self._post_json_with_retries(
            f"{self.settings.provider_base_url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json={
                'model': self.settings.provider_model,
                'messages': self._build_summary_messages(previous_summary=previous_summary, messages=messages, locale=locale, max_chars=max_chars),
                'temperature': 0.1,
            },
        )
        choices = payload.get('choices') or []
        if not choices:
            return None
        summary = (choices[0].get('message') or {}).get('content')
        return self._clean_summary(summary, max_chars=max_chars)

    def _build_summary_messages(
        self,
        *,
        previous_summary: str | None,
        messages: list[dict[str, str]],
        locale: str,
        max_chars: int,
    ) -> list[dict[str, str]]:
        preferred_language = locale_language_name(locale)
        transcript = '\n'.join(
            f"{item.get('role', 'message')}: {(item.get('text') or '').strip()}"
            for item in messages
            if (item.get('text') or '').strip()
        )
        return [
            {
                'role': 'system',
                'content': (
                    'Create a compact private conversation summary for a portfolio assistant. '
                    'Keep only details that help answer follow-up questions in this same chat: user intent, preferences, entities discussed, decisions, and unresolved questions. '
                    'Do not include private implementation details. Do not invent facts. '
                    f'Keep it under {max_chars} characters. Write in {preferred_language} when possible.'
                ),
            },
            {
                'role': 'user',
                'content': (
                    f'Previous summary:\n{previous_summary or "None yet."}\n\n'
                    f'Recent messages:\n{transcript}\n\n'
                    'Return only the updated summary.'
                ),
            },
        ]

    def _summarize_locally(self, *, previous_summary: str | None, messages: list[dict[str, str]], max_chars: int) -> str | None:
        user_messages = [
            (item.get('text') or '').strip()
            for item in messages
            if item.get('role') == 'user' and (item.get('text') or '').strip()
        ]
        if not user_messages and not previous_summary:
            return None
        seed = (previous_summary or '').strip()
        latest = ' | '.join(user_messages[-4:])
        summary = f'{seed}\nRecent visitor topics/questions: {latest}'.strip() if seed else f'Recent visitor topics/questions: {latest}'
        return self._clean_summary(summary, max_chars=max_chars)

    def _clean_summary(self, summary: object, *, max_chars: int) -> str | None:
        if not isinstance(summary, str):
            return None
        cleaned = ' '.join(summary.strip().split())
        if not cleaned:
            return None
        if len(cleaned) > max_chars:
            cleaned = cleaned[: max_chars - 3].rstrip() + '...'
        return cleaned

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
