from __future__ import annotations

import os
from pathlib import Path

from fastapi.testclient import TestClient


def test_portfolio_docs_are_disabled_in_production(tmp_path: Path) -> None:
    database_path = tmp_path / 'portfolio-production.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['APP_ENV'] = 'production'
    os.environ['MEDIA_PUBLIC_BASE_URL'] = 'http://media.example.test'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'test-admin-pass'

    from app.core.config import get_settings
    from app.db.session import reset_database_caches
    from infra.postgres.bootstrap.bootstrap_core import initialize_database

    get_settings.cache_clear()
    reset_database_caches()
    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

    from app.main import create_app

    with TestClient(create_app()) as client:
        assert client.get('/docs').status_code == 404
        assert client.get('/openapi.json').status_code == 404

    get_settings.cache_clear()
    reset_database_caches()