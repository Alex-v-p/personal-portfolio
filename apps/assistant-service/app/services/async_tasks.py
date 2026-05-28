from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
import json
from typing import Any
from uuid import uuid4

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import get_settings

CHAT_RESPONSE_TASK = 'chat-response'


class TaskQueueUnavailable(RuntimeError):
    pass


@dataclass(slots=True)
class ChatTaskEnvelope:
    task_id: str
    task_type: str
    payload: dict[str, Any]
    submitted_at: str


@dataclass(slots=True)
class ChatTaskRecord:
    task_id: str
    task_type: str
    status: str
    submitted_at: str
    started_at: str | None = None
    completed_at: str | None = None
    error_message: str | None = None
    result: dict[str, Any] | None = None


@lru_cache
def _redis_client(redis_url: str) -> Redis:
    return Redis.from_url(redis_url, decode_responses=True)


class ChatTaskQueue:
    def __init__(self, redis_url: str, *, ttl_seconds: int = 3600 * 24) -> None:
        self.redis_url = redis_url.strip()
        self.ttl_seconds = ttl_seconds
        self.queue_key = 'assistant:chat:tasks:queue'
        self.processing_key = 'assistant:chat:tasks:processing'
        self.task_key_prefix = 'assistant:chat:tasks:'

    @property
    def enabled(self) -> bool:
        return bool(self.redis_url) and not self.redis_url.startswith('memory://')

    @property
    def poll_after_ms(self) -> int:
        return 900

    def enqueue(self, task_type: str, payload: dict[str, Any]) -> ChatTaskRecord:
        client = self._client()
        task_id = str(uuid4())
        submitted_at = _now_iso()
        raw_envelope = _json_dumps(
            {
                'task_id': task_id,
                'task_type': task_type,
                'payload': payload,
                'submitted_at': submitted_at,
            }
        )
        try:
            pipeline = client.pipeline()
            pipeline.hset(
                self._task_key(task_id),
                mapping={
                    'task_id': task_id,
                    'task_type': task_type,
                    'status': 'queued',
                    'submitted_at': submitted_at,
                    'payload_json': _json_dumps(payload),
                },
            )
            pipeline.expire(self._task_key(task_id), self.ttl_seconds)
            pipeline.rpush(self.queue_key, raw_envelope)
            pipeline.execute()
        except RedisError as exc:
            raise TaskQueueUnavailable('Redis chat queue is unavailable.') from exc
        return ChatTaskRecord(task_id=task_id, task_type=task_type, status='queued', submitted_at=submitted_at)

    def get(self, task_id: str) -> ChatTaskRecord | None:
        client = self._client()
        try:
            data = client.hgetall(self._task_key(task_id))
        except RedisError as exc:
            raise TaskQueueUnavailable('Redis chat queue is unavailable.') from exc
        if not data:
            return None
        return ChatTaskRecord(
            task_id=data.get('task_id', task_id),
            task_type=data.get('task_type', ''),
            status=data.get('status', 'queued'),
            submitted_at=data.get('submitted_at', ''),
            started_at=data.get('started_at') or None,
            completed_at=data.get('completed_at') or None,
            error_message=data.get('error_message') or None,
            result=_json_loads(data.get('result_json')),
        )

    def restore_processing_tasks(self) -> int:
        client = self._client()
        try:
            raw_items = client.lrange(self.processing_key, 0, -1)
            if not raw_items:
                return 0
            pipeline = client.pipeline()
            pipeline.delete(self.processing_key)
            for raw_item in raw_items:
                task_id = _task_id_from_raw(raw_item)
                if task_id:
                    pipeline.hset(
                        self._task_key(task_id),
                        mapping={'status': 'queued', 'started_at': '', 'completed_at': '', 'error_message': ''},
                    )
                    pipeline.expire(self._task_key(task_id), self.ttl_seconds)
                pipeline.lpush(self.queue_key, raw_item)
            pipeline.execute()
            return len(raw_items)
        except RedisError as exc:
            raise TaskQueueUnavailable('Redis chat queue is unavailable.') from exc

    def reserve(self, *, timeout_seconds: int = 5) -> tuple[ChatTaskEnvelope, str] | None:
        client = self._client()
        try:
            raw_item = client.brpoplpush(self.queue_key, self.processing_key, timeout=timeout_seconds)
        except RedisError as exc:
            raise TaskQueueUnavailable('Redis chat queue is unavailable.') from exc
        if raw_item is None:
            return None
        data = _json_loads(raw_item) or {}
        envelope = ChatTaskEnvelope(
            task_id=str(data.get('task_id') or ''),
            task_type=str(data.get('task_type') or ''),
            payload=data.get('payload') if isinstance(data.get('payload'), dict) else {},
            submitted_at=str(data.get('submitted_at') or ''),
        )
        self.mark_running(envelope.task_id)
        return envelope, raw_item

    def mark_running(self, task_id: str) -> None:
        client = self._client()
        try:
            pipeline = client.pipeline()
            pipeline.hset(self._task_key(task_id), mapping={'status': 'running', 'started_at': _now_iso(), 'error_message': ''})
            pipeline.expire(self._task_key(task_id), self.ttl_seconds)
            pipeline.execute()
        except RedisError as exc:
            raise TaskQueueUnavailable('Redis chat queue is unavailable.') from exc

    def mark_succeeded(self, task_id: str, *, result: dict[str, Any], raw_item: str) -> None:
        self._finish(task_id, raw_item=raw_item, status='succeeded', result=result, error_message=None)

    def mark_failed(self, task_id: str, *, error_message: str, raw_item: str) -> None:
        self._finish(task_id, raw_item=raw_item, status='failed', result=None, error_message=error_message)

    def _finish(self, task_id: str, *, raw_item: str, status: str, result: dict[str, Any] | None, error_message: str | None) -> None:
        client = self._client()
        try:
            pipeline = client.pipeline()
            mapping = {'status': status, 'completed_at': _now_iso(), 'error_message': error_message or ''}
            if result is not None:
                mapping['result_json'] = _json_dumps(result)
            pipeline.hset(self._task_key(task_id), mapping=mapping)
            pipeline.expire(self._task_key(task_id), self.ttl_seconds)
            pipeline.lrem(self.processing_key, 1, raw_item)
            pipeline.execute()
        except RedisError as exc:
            raise TaskQueueUnavailable('Redis chat queue is unavailable.') from exc

    def _client(self) -> Redis:
        if not self.enabled:
            raise TaskQueueUnavailable('Redis chat queue is disabled.')
        return _redis_client(self.redis_url)

    def _task_key(self, task_id: str) -> str:
        return f'{self.task_key_prefix}{task_id}'


@lru_cache
def get_chat_task_queue() -> ChatTaskQueue:
    settings = get_settings()
    return ChatTaskQueue(settings.redis_url)


def reset_chat_task_queue_cache() -> None:
    get_chat_task_queue.cache_clear()
    _redis_client.cache_clear()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_dumps(value: Any) -> str:
    return json.dumps(value, separators=(',', ':'), ensure_ascii=False)


def _json_loads(value: str | None) -> dict[str, Any] | None:
    if not value:
        return None
    data = json.loads(value)
    return data if isinstance(data, dict) else None


def _task_id_from_raw(raw_item: str) -> str | None:
    data = _json_loads(raw_item)
    task_id = data.get('task_id') if isinstance(data, dict) else None
    return str(task_id) if task_id else None
