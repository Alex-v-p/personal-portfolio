from __future__ import annotations

import re
from typing import Iterable

from app.services.retrieval.constants import _SMALLTALK_PATTERNS, _STOP_WORDS


def metadata_text(metadata: dict | None) -> str:
    if not metadata:
        return ''
    values: list[str] = []
    for value in metadata.values():
        if isinstance(value, str):
            values.append(value.lower())
        elif isinstance(value, list):
            values.extend(str(item).lower() for item in value)
    return ' '.join(values)


def tokenize(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]{1,}", text.lower()) if token not in _STOP_WORDS]


def excerpt(text: str, tokens: Iterable[str], limit: int = 300) -> str:
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


def parse_vector(value: object) -> list[float] | None:
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


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip().lower()


def contains_any(text: str, phrases: set[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def is_smalltalk(text: str) -> bool:
    if not text:
        return True
    if text in _SMALLTALK_PATTERNS:
        return True
    tokens = [token for token in re.findall(r"[a-zA-Z0-9']+", text) if token]
    if len(tokens) <= 3 and all(token in {'hi', 'hello', 'hey', 'thanks', 'thank', 'yo'} for token in tokens):
        return True
    return False
