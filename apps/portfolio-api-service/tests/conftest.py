from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.session import reset_database_caches


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    database_path = tmp_path / 'portfolio-test.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['DB_AUTO_CREATE'] = 'true'
    os.environ['DB_AUTO_SEED'] = 'true'
    os.environ['DB_STARTUP_GRACEFUL'] = 'false'
    get_settings.cache_clear()
    reset_database_caches()

    from app.main import create_app

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client

    get_settings.cache_clear()
    reset_database_caches()
