from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

from app.services.rate_limit import rate_limiter


def derive_request_identifier(request: Request | None, *candidates: str | None) -> str:
    parts: list[str] = []
    for candidate in candidates:
        if candidate and candidate.strip():
            parts.append(candidate.strip()[:180])
            break

    request_ip = _extract_request_ip(request)
    if request_ip:
        parts.append(request_ip[:60])

    if parts:
        return '|'.join(parts)[:255]
    return 'anonymous'


def _extract_request_ip(request: Request | None) -> str | None:
    if request is None:
        return None
    forwarded_for = request.headers.get('x-forwarded-for')
    if forwarded_for:
        first = forwarded_for.split(',')[0].strip()
        if first:
            return first
    real_ip = request.headers.get('x-real-ip')
    if real_ip and real_ip.strip():
        return real_ip.strip()
    client = getattr(request, 'client', None)
    host = getattr(client, 'host', None)
    return str(host) if host else None


def enforce_rate_limit_or_429(*, scope: str, identifier: str, limit: int, window_seconds: int, detail: str) -> None:
    decision = rate_limiter.hit(scope=scope, identifier=identifier, limit=limit, window_seconds=window_seconds)
    if decision.allowed:
        return
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=detail,
        headers={'Retry-After': str(decision.retry_after_seconds)},
    )


def ensure_payload_size_within_limit(payload: BaseModel | dict[str, Any], *, max_bytes: int, detail: str) -> None:
    if max_bytes <= 0:
        return
    if isinstance(payload, BaseModel):
        payload_bytes = payload.model_dump_json(by_alias=True).encode('utf-8')
    else:
        payload_bytes = str(payload).encode('utf-8')
    if len(payload_bytes) > max_bytes:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=detail)


def sanitize_event_metadata(
    metadata: dict[str, Any] | None,
    *,
    max_entries: int,
    max_depth: int,
    max_list_items: int,
    max_string_length: int,
) -> dict[str, Any] | None:
    if not metadata:
        return None

    sanitized: dict[str, Any] = {}
    for index, (raw_key, raw_value) in enumerate(metadata.items()):
        if index >= max_entries:
            break
        key = str(raw_key).strip()[:80]
        if not key:
            continue
        sanitized[key] = _sanitize_json_like(
            raw_value,
            depth=1,
            max_depth=max_depth,
            max_entries=max_entries,
            max_list_items=max_list_items,
            max_string_length=max_string_length,
        )
    return sanitized or None


def _sanitize_json_like(value: Any, *, depth: int, max_depth: int, max_entries: int, max_list_items: int, max_string_length: int) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value[:max_string_length]
    if depth >= max_depth:
        return str(value)[:max_string_length]
    if isinstance(value, dict):
        nested: dict[str, Any] = {}
        for index, (raw_key, raw_value) in enumerate(value.items()):
            if index >= max_entries:
                break
            key = str(raw_key).strip()[:80]
            if not key:
                continue
            nested[key] = _sanitize_json_like(
                raw_value,
                depth=depth + 1,
                max_depth=max_depth,
                max_entries=max_entries,
                max_list_items=max_list_items,
                max_string_length=max_string_length,
            )
        return nested
    if isinstance(value, (list, tuple, set)):
        return [
            _sanitize_json_like(
                item,
                depth=depth + 1,
                max_depth=max_depth,
                max_entries=max_entries,
                max_list_items=max_list_items,
                max_string_length=max_string_length,
            )
            for item in list(value)[:max_list_items]
        ]
    return str(value)[:max_string_length]
