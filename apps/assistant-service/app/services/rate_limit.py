from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import lru_cache

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import get_settings


@dataclass(slots=True)
class RateLimitDecision:
    allowed: bool
    retry_after_seconds: int
    attempts: int


class _InMemoryCounterStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: dict[str, tuple[int, float]] = {}

    def increment(self, key: str, window_seconds: int) -> tuple[int, int]:
        now = time.time()
        with self._lock:
            count, expires_at = self._entries.get(key, (0, now + window_seconds))
            if expires_at <= now:
                count = 0
                expires_at = now + window_seconds
            count += 1
            self._entries[key] = (count, expires_at)
            self._purge(now)
            retry_after = max(1, int(expires_at - now))
            return count, retry_after

    def increment_daily(self, key: str) -> tuple[int, int]:
        now = datetime.now(timezone.utc)
        tomorrow = datetime.combine((now + timedelta(days=1)).date(), datetime.min.time(), tzinfo=timezone.utc)
        ttl_seconds = max(int((tomorrow - now).total_seconds()), 1)
        with self._lock:
            count, expires_at = self._entries.get(key, (0, time.time() + ttl_seconds))
            if expires_at <= time.time():
                count = 0
                expires_at = time.time() + ttl_seconds
            count += 1
            self._entries[key] = (count, expires_at)
            self._purge(time.time())
            return count, ttl_seconds

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()

    def _purge(self, now: float) -> None:
        expired = [key for key, (_, expires_at) in self._entries.items() if expires_at <= now]
        for key in expired:
            self._entries.pop(key, None)


_memory_store = _InMemoryCounterStore()


@lru_cache
def get_redis_client() -> Redis | None:
    settings = get_settings()
    redis_url = settings.redis_url.strip()
    if not redis_url or redis_url.startswith('memory://'):
        return None

    client = Redis.from_url(redis_url, decode_responses=True)
    try:
        client.ping()
    except RedisError:
        return None
    return client


class RateLimiter:
    def hit(self, *, scope: str, identifier: str, limit: int, window_seconds: int) -> RateLimitDecision:
        key = f'assistant-rate-limit:{scope}:{identifier}'
        if limit <= 0 or window_seconds <= 0:
            return RateLimitDecision(allowed=True, retry_after_seconds=0, attempts=1)

        client = get_redis_client()
        if client is not None:
            try:
                attempts = int(client.incr(key))
                if attempts == 1:
                    client.expire(key, window_seconds)
                retry_after = max(int(client.ttl(key)), 1)
                return RateLimitDecision(allowed=attempts <= limit, retry_after_seconds=retry_after, attempts=attempts)
            except RedisError:
                pass

        attempts, retry_after = _memory_store.increment(key=key, window_seconds=window_seconds)
        return RateLimitDecision(allowed=attempts <= limit, retry_after_seconds=retry_after, attempts=attempts)


class ProviderBudgetGuard:
    def consume_generation_budget(self, *, scope: str, daily_limit: int) -> bool:
        if daily_limit <= 0:
            return False
        day_key = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        key = f'assistant-provider-budget:{scope}:{day_key}'
        client = get_redis_client()
        if client is not None:
            try:
                attempts = int(client.incr(key))
                if attempts == 1:
                    now = datetime.now(timezone.utc)
                    tomorrow = datetime.combine((now + timedelta(days=1)).date(), datetime.min.time(), tzinfo=timezone.utc)
                    ttl_seconds = max(int((tomorrow - now).total_seconds()), 1)
                    client.expire(key, ttl_seconds)
                return attempts <= daily_limit
            except RedisError:
                pass

        attempts, _ = _memory_store.increment_daily(key=key)
        return attempts <= daily_limit


rate_limiter = RateLimiter()
provider_budget_guard = ProviderBudgetGuard()


def reset_rate_limit_state() -> None:
    get_redis_client.cache_clear()
    _memory_store.clear()
