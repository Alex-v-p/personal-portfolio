from __future__ import annotations

import os

import pytest

_ASSISTANT_TEST_ENV_DEFAULTS = {
    'REDIS_URL': 'memory://',
    'CHAT_RATE_LIMIT_MAX_REQUESTS': '12',
    'CHAT_RATE_LIMIT_WINDOW_SECONDS': '60',
    'CHAT_MAX_REQUEST_BYTES': '16384',
    'PROVIDER_DAILY_GENERATION_CAP': '1000',
    'ASSISTANT_PROVIDER_BACKEND': 'mock',
}


@pytest.fixture(autouse=True)
def _isolate_assistant_test_environment() -> None:
    previous_values = {key: os.environ.get(key) for key in _ASSISTANT_TEST_ENV_DEFAULTS}
    for key, value in _ASSISTANT_TEST_ENV_DEFAULTS.items():
        os.environ[key] = value

    _clear_runtime_caches()

    from app.services.async_tasks import reset_chat_task_queue_cache
    from app.services.rate_limit import reset_rate_limit_state

    reset_rate_limit_state()
    reset_chat_task_queue_cache()
    yield
    for key, previous_value in previous_values.items():
        if previous_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = previous_value

    _clear_runtime_caches()
    reset_rate_limit_state()
    reset_chat_task_queue_cache()


def _clear_runtime_caches() -> None:
    from app.core.config import get_settings
    from app.db.session import get_engine, get_session_factory

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
