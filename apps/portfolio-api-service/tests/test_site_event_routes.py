from __future__ import annotations

import os
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.session import reset_database_caches
from app.services.rate_limit import reset_rate_limit_state
from infra.postgres.bootstrap.bootstrap_core import initialize_database


def _build_client(tmp_path: Path, **env: str) -> TestClient:
    database_path = tmp_path / 'portfolio-events.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['MEDIA_PUBLIC_BASE_URL'] = 'http://media.example.test'
    os.environ['REDIS_URL'] = 'memory://'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'test-admin-pass'
    os.environ['ADMIN_DISPLAY_NAME'] = 'Test Admin'
    for key, value in env.items():
        os.environ[key] = value
    get_settings.cache_clear()
    reset_database_caches()
    reset_rate_limit_state()
    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

    from app.main import create_app

    return TestClient(create_app())


def test_create_site_event_is_rate_limited(tmp_path: Path) -> None:
    with _build_client(
        tmp_path,
        EVENTS_RATE_LIMIT_MAX_REQUESTS='1',
        EVENTS_RATE_LIMIT_WINDOW_SECONDS='60',
    ) as client:
        payload = {
            'eventType': 'page_view',
            'pagePath': '/projects',
            'visitorId': 'visitor-1',
            'sessionId': 'session-1',
            'metadata': {'route': '/projects'},
        }
        first = client.post('/api/events', json=payload)
        second = client.post('/api/events', json=payload)

    assert first.status_code == 201
    assert second.status_code == 429
    assert second.json()['detail'] == 'Too many site events were submitted in a short period. Please slow down.'
