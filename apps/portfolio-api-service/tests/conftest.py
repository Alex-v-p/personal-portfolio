from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


from app.core.config import get_settings
from app.db.session import reset_database_caches
from infra.postgres.bootstrap.bootstrap_core import initialize_database


REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))



@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    database_path = tmp_path / 'portfolio-test.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['MEDIA_PUBLIC_BASE_URL'] = 'http://media.example.test'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'test-admin-pass'
    os.environ['ADMIN_DISPLAY_NAME'] = 'Test Admin'
    get_settings.cache_clear()
    reset_database_caches()

    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

    from app.main import create_app

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client

    get_settings.cache_clear()
    reset_database_caches()
