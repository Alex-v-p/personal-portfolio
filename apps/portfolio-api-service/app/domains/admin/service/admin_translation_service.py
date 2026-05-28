from __future__ import annotations

import logging
import re
from dataclasses import dataclass

import httpx
from fastapi import HTTPException, status

from app.core.config import get_settings
from app.domains.admin.schema import AdminTranslationDraftIn, AdminTranslationDraftOut

logger = logging.getLogger(__name__)


@dataclass
class _ProviderConfig:
    backend: str
    model: str
    base_url: str
    api_key: str
    timeout_seconds: float
    max_retries: int


class AdminTranslationDraftService:
    def __init__(self) -> None:
        settings = get_settings()
        self.config = _ProviderConfig(
            backend=settings.translation_provider_backend.strip().lower(),
            model=settings.translation_provider_model,
            base_url=settings.translation_provider_base_url.rstrip('/'),
            api_key=settings.translation_provider_api_key.strip(),
            timeout_seconds=settings.translation_provider_request_timeout_seconds,
            max_retries=max(settings.translation_provider_max_retries, 0),
        )

    def generate_draft(self, payload: AdminTranslationDraftIn) -> AdminTranslationDraftOut:
        fields = {key: value for key, value in payload.fields.items() if isinstance(value, str) and value.strip()}
        if not fields:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Provide at least one non-empty field to translate.')
        if payload.source_locale == payload.target_locale:
            return AdminTranslationDraftOut(
                source_locale=payload.source_locale,
                target_locale=payload.target_locale,
                entity_type=payload.entity_type,
                translated_fields=fields,
                provider_backend='passthrough',
                provider_model=None,
                warnings=['Source and target locale are identical, so the original text was returned unchanged.'],
            )

        translated_fields, warnings = self._translate_fields(payload=payload, fields=fields)
        return AdminTranslationDraftOut(
            source_locale=payload.source_locale,
            target_locale=payload.target_locale,
            entity_type=payload.entity_type,
            translated_fields=translated_fields,
            provider_backend=self.config.backend,
            provider_model=self.config.model,
            warnings=warnings,
        )

    def _translate_fields(self, *, payload: AdminTranslationDraftIn, fields: dict[str, str]) -> tuple[dict[str, str], list[str]]:
        backend = self.config.backend
        if backend == 'mock':
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail='Translation drafts are disabled because no live translation-capable provider is configured. Set the translation or assistant provider environment variables first.',
            )
        if backend not in {'ollama', 'openai-compatible', 'openai_compatible', 'vllm'}:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f'Unsupported translation provider backend: {self.config.backend}.')

        translated: dict[str, str] = {}
        warnings: list[str] = []
        for key, value in fields.items():
            rendered = self._translate_single_field(payload=payload, field_key=key, value=value)
            cleaned = rendered.strip()
            if not cleaned:
                warnings.append(f'{key} returned empty text and needs manual review.')
                continue

            translated[key] = cleaned
            if self._field_needs_review(field_key=key, source=value, translated=cleaned):
                warnings.append(f'{key} was returned unchanged and may still need translation review.')

        if not translated:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='The translation provider did not return any usable translated fields.')
        return translated, warnings

    def _translate_single_field(self, *, payload: AdminTranslationDraftIn, field_key: str, value: str) -> str:
        if self._should_chunk_field(field_key=field_key, value=value):
            translated = self._translate_chunked_text(payload=payload, field_key=field_key, value=value)
        else:
            translated = self._translate_text(payload=payload, field_key=field_key, value=value)

        if self._should_retry_unchanged(field_key=field_key, source=value, translated=translated):
            retry_translated = self._translate_text(payload=payload, field_key=field_key, value=value, strict=True)
            if retry_translated.strip():
                translated = retry_translated
        return translated

    def _translate_chunked_text(self, *, payload: AdminTranslationDraftIn, field_key: str, value: str) -> str:
        parts: list[str] = []
        for is_translatable, segment in self._split_code_fence_segments(value):
            if not is_translatable:
                parts.append(segment)
                continue
            for chunk in self._split_translatable_segment(segment):
                parts.append(self._translate_text(payload=payload, field_key=field_key, value=chunk, markdown=True))
        return ''.join(parts)

    def _translate_text(
        self,
        *,
        payload: AdminTranslationDraftIn,
        field_key: str,
        value: str,
        markdown: bool | None = None,
        strict: bool = False,
    ) -> str:
        preserve_markdown = self._is_markdown_field(field_key) if markdown is None else markdown
        backend = self.config.backend
        if backend == 'ollama':
            return self._translate_text_with_ollama(
                payload=payload,
                field_key=field_key,
                value=value,
                preserve_markdown=preserve_markdown,
                strict=strict,
            )
        return self._translate_text_with_openai_compatible(
            payload=payload,
            field_key=field_key,
            value=value,
            preserve_markdown=preserve_markdown,
            strict=strict,
        )

    def _translate_text_with_ollama(
        self,
        *,
        payload: AdminTranslationDraftIn,
        field_key: str,
        value: str,
        preserve_markdown: bool,
        strict: bool,
    ) -> str:
        messages = self._build_field_messages(
            payload=payload,
            field_key=field_key,
            value=value,
            preserve_markdown=preserve_markdown,
            strict=strict,
        )
        chat_payload = {
            'model': self.config.model,
            'stream': False,
            'messages': messages,
            'options': {'temperature': 0.05},
        }
        generate_payload = {
            'model': self.config.model,
            'stream': False,
            'prompt': self._build_ollama_generate_prompt(messages),
            'options': {'temperature': 0.05},
        }
        response = self._post_json_with_retries(
            self._candidate_ollama_urls(),
            request_specs=[{'json': chat_payload}, {'json': generate_payload}],
        )
        return self._extract_text_response(response)

    def _translate_text_with_openai_compatible(
        self,
        *,
        payload: AdminTranslationDraftIn,
        field_key: str,
        value: str,
        preserve_markdown: bool,
        strict: bool,
    ) -> str:
        headers = {'Content-Type': 'application/json'}
        if self.config.api_key:
            headers['Authorization'] = f'Bearer {self.config.api_key}'
        response = self._post_json_with_retries(
            self._candidate_openai_urls(),
            request_specs=[{
                'headers': headers,
                'json': {
                    'model': self.config.model,
                    'messages': self._build_field_messages(
                        payload=payload,
                        field_key=field_key,
                        value=value,
                        preserve_markdown=preserve_markdown,
                        strict=strict,
                    ),
                    'temperature': 0.05,
                },
            }],
        )
        return self._extract_text_response(response)

    def _candidate_ollama_urls(self) -> list[str]:
        base = self.config.base_url.rstrip('/')
        if base.endswith('/api/chat'):
            return [base, f"{base[:-5]}/generate"]
        if base.endswith('/api/generate'):
            return [base[:-8] + '/chat', base]
        if base.endswith('/api'):
            return [f'{base}/chat', f'{base}/generate']
        return [f'{base}/api/chat', f'{base}/api/generate']

    def _candidate_openai_urls(self) -> list[str]:
        base = self.config.base_url.rstrip('/')
        if base.endswith('/v1/chat/completions') or base.endswith('/chat/completions'):
            return [base]
        if base.endswith('/v1'):
            return [f'{base}/chat/completions', f'{base}/completions']
        return [f'{base}/v1/chat/completions', f'{base}/chat/completions']

    def _build_ollama_generate_prompt(self, messages: list[dict[str, str]]) -> str:
        return '\n\n'.join(f"{message['role'].upper()}: {message['content']}" for message in messages)

    def _build_field_messages(
        self,
        *,
        payload: AdminTranslationDraftIn,
        field_key: str,
        value: str,
        preserve_markdown: bool,
        strict: bool,
    ) -> list[dict[str, str]]:
        field_kind = self._describe_field_kind(field_key)
        instructions = [
            'You translate CMS draft content for a developer portfolio website.',
            f'Translate from {payload.source_locale} to {payload.target_locale}.',
            f'Return only the translated {field_kind} text for this single field.',
            'Do not return JSON, arrays, explanations, or commentary.',
            'Keep names, URLs, slugs, filenames, email addresses, code, and technology or brand names unchanged unless they are ordinary prose.',
            'Keep the tone professional, natural, and concise where appropriate.',
        ]
        if preserve_markdown:
            instructions.extend([
                'Preserve markdown structure exactly where possible, including headings, emphasis, bullet lists, numbered lists, blockquotes, and links.',
                'Do not change code fences, inline code, URLs, or image/link destinations.',
            ])
        if strict:
            instructions.append('Translate ordinary prose fully. Do not leave English unchanged unless it is clearly a proper noun, brand, URL, code term, or other non-translatable token.')

        context = payload.context.strip() if payload.context else ''
        user_lines = [
            f'Entity type: {payload.entity_type}',
            f'Field key: {field_key}',
        ]
        if context:
            user_lines.append(f'Additional context: {context}')
        user_lines.append('Source text:')
        user_lines.append(value)
        return [
            {'role': 'system', 'content': ' '.join(instructions)},
            {'role': 'user', 'content': '\n'.join(user_lines)},
        ]

    def _extract_text_response(self, payload: dict) -> str:
        candidates = []
        message = payload.get('message') if isinstance(payload, dict) else None
        if isinstance(message, dict):
            candidates.append(message.get('content'))
        if isinstance(payload, dict):
            candidates.append(payload.get('response'))
            choices = payload.get('choices')
            if isinstance(choices, list) and choices:
                first_choice = choices[0] if isinstance(choices[0], dict) else None
                if isinstance(first_choice, dict):
                    msg = first_choice.get('message')
                    if isinstance(msg, dict):
                        candidates.append(msg.get('content'))
                    candidates.append(first_choice.get('text'))
        for candidate in candidates:
            text = self._coerce_text(candidate)
            if text:
                return text.strip()
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='The translation provider returned an empty response.')

    def _coerce_text(self, value) -> str | None:
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            text_parts: list[str] = []
            for item in value:
                if isinstance(item, str):
                    text_parts.append(item)
                    continue
                if not isinstance(item, dict):
                    continue
                text_candidate = item.get('text') or item.get('content')
                if isinstance(text_candidate, str):
                    text_parts.append(text_candidate)
            combined = ''.join(text_parts).strip()
            return combined or None
        return None

    def _describe_field_kind(self, field_key: str) -> str:
        key = field_key.lower()
        if 'markdown' in key:
            return 'markdown'
        if 'title' in key:
            return 'title'
        if 'summary' in key or 'excerpt' in key or 'teaser' in key or 'intro' in key:
            return 'summary'
        if 'description' in key:
            return 'description'
        if 'alt' in key:
            return 'alt text'
        if 'label' in key or 'name' in key or 'status' in key:
            return 'label'
        return 'text'

    def _is_markdown_field(self, field_key: str) -> bool:
        return 'markdown' in field_key.lower()

    def _should_chunk_field(self, *, field_key: str, value: str) -> bool:
        return self._is_markdown_field(field_key) or len(value) > 1800

    def _should_retry_unchanged(self, *, field_key: str, source: str, translated: str) -> bool:
        if not translated.strip():
            return False
        if source.strip() != translated.strip():
            return False
        if self._is_markdown_field(field_key):
            return False
        if re.fullmatch(r'[\w .:/#@+\-()]+', source.strip()) is None:
            return False
        words = re.findall(r'[A-Za-z]{3,}', source)
        return len(words) >= 3

    def _field_needs_review(self, *, field_key: str, source: str, translated: str) -> bool:
        if not translated.strip() or source.strip() != translated.strip():
            return False
        if self._is_markdown_field(field_key):
            return len(re.findall(r'[A-Za-z]{3,}', source)) >= 12
        return self._should_retry_unchanged(field_key=field_key, source=source, translated=translated)

    def _split_code_fence_segments(self, value: str) -> list[tuple[bool, str]]:
        pattern = re.compile(r'(```[\s\S]*?```|~~~[\s\S]*?~~~)')
        parts: list[tuple[bool, str]] = []
        last_index = 0
        for match in pattern.finditer(value):
            start, end = match.span()
            if start > last_index:
                parts.append((True, value[last_index:start]))
            parts.append((False, value[start:end]))
            last_index = end
        if last_index < len(value):
            parts.append((True, value[last_index:]))
        return parts or [(True, value)]

    def _split_translatable_segment(self, text: str, *, max_chars: int = 1600) -> list[str]:
        if len(text) <= max_chars:
            return [text]
        units = re.split(r'(\n\s*\n)', text)
        chunks: list[str] = []
        current = ''
        for unit in units:
            if not unit:
                continue
            if len(unit) > max_chars:
                for piece in self._split_large_unit(unit, max_chars=max_chars):
                    if current:
                        chunks.append(current)
                        current = ''
                    chunks.append(piece)
                continue
            if current and len(current) + len(unit) > max_chars:
                chunks.append(current)
                current = unit
            else:
                current += unit
        if current:
            chunks.append(current)
        return chunks

    def _split_large_unit(self, unit: str, *, max_chars: int) -> list[str]:
        lines = re.split(r'(\n)', unit)
        pieces: list[str] = []
        current = ''
        for line in lines:
            if not line:
                continue
            if len(current) + len(line) > max_chars and current:
                pieces.append(current)
                current = line
            else:
                current += line
        if current:
            pieces.append(current)
        return pieces or [unit]

    def _post_json_with_retries(self, urls: str | list[str], *, request_specs: list[dict] | None = None, **kwargs) -> dict:
        candidate_urls = [urls] if isinstance(urls, str) else list(dict.fromkeys(urls))
        candidate_request_specs = request_specs or [kwargs]
        last_error: Exception | None = None
        for url in candidate_urls:
            for request_spec in candidate_request_specs:
                attempts = self.config.max_retries + 1
                for _ in range(attempts):
                    try:
                        with httpx.Client(timeout=self.config.timeout_seconds) as client:
                            response = client.post(url, **request_spec)
                            response.raise_for_status()
                            return response.json()
                    except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as exc:
                        last_error = exc
                        if not self._should_retry(exc=exc):
                            break
        if isinstance(last_error, httpx.TimeoutException):
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail='The translation provider timed out while generating a draft.') from last_error
        if isinstance(last_error, httpx.NetworkError):
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='The translation provider could not be reached.') from last_error
        if isinstance(last_error, httpx.HTTPStatusError):
            body = last_error.response.text.strip()[:400]
            if last_error.response.status_code == status.HTTP_404_NOT_FOUND:
                if 'model' in body.lower() and 'not found' in body.lower():
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail='The configured translation model was not found on the provider. Pull the model locally or update the configured translation model name.',
                    ) from last_error
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail='The translation provider endpoint was not found (HTTP 404). Check the configured backend/base URL, or update to a provider that supports the translation endpoint.',
                ) from last_error
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f'The translation provider returned HTTP {last_error.response.status_code}.') from last_error
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='The translation provider could not be reached.')

    def _should_retry(self, *, exc: Exception) -> bool:
        if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
            return True
        if isinstance(exc, httpx.HTTPStatusError):
            return exc.response.status_code in {408, 429, 500, 502, 503, 504}
        return False
