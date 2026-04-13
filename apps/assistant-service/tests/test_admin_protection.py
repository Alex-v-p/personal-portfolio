from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import text


def _build_admin_token(secret_key: str, admin_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub': admin_id,
        'email': 'admin@example.com',
        'type': 'admin-access',
        'exp': now + timedelta(minutes=30),
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def test_admin_only_assistant_endpoints_require_valid_token(tmp_path: Path) -> None:
    database_path = tmp_path / 'assistant-auth.sqlite3'
    secret_key = 'test-secret-key'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['SECRET_KEY'] = secret_key
    os.environ['ASSISTANT_PROVIDER_BACKEND'] = 'mock'

    from app.core.config import get_settings
    from app.db.models import Base
    from app.db.session import get_engine, get_session_factory

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    engine = get_engine()
    Base.metadata.create_all(engine)

    admin_id = str(uuid4())
    with engine.begin() as connection:
        connection.execute(
            text(
                'CREATE TABLE admin_users ('
                'id CHAR(32) PRIMARY KEY, '
                'email VARCHAR(320) NOT NULL, '
                'password_hash VARCHAR(255) NOT NULL, '
                'display_name VARCHAR(120) NOT NULL, '
                'is_active BOOLEAN NOT NULL, '
                'created_at DATETIME NOT NULL'
                ')'
            )
        )
        connection.execute(
            text(
                'INSERT INTO admin_users (id, email, password_hash, display_name, is_active, created_at) '
                'VALUES (:id, :email, :password_hash, :display_name, :is_active, :created_at)'
            ),
            {
                'id': admin_id,
                'email': 'admin@example.com',
                'password_hash': 'unused',
                'display_name': 'Admin',
                'is_active': True,
                'created_at': datetime.now(timezone.utc),
            },
        )

    token = _build_admin_token(secret_key, admin_id)

    from app.main import create_app

    with TestClient(create_app()) as client:
        assert client.get('/api/conversations').status_code == 401
        assert client.get('/api/providers').status_code == 401
        assert client.get('/api/knowledge/status').status_code == 401

        headers = {'Authorization': f'Bearer {token}'}
        assert client.get('/api/conversations', headers=headers).status_code == 200
        assert client.get('/api/providers', headers=headers).status_code == 200
        assert client.get('/api/knowledge/status', headers=headers).status_code == 200


def test_assistant_docs_are_disabled_in_production(tmp_path: Path) -> None:
    database_path = tmp_path / 'assistant-production.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['APP_ENV'] = 'production'

    from app.core.config import get_settings
    from app.db.models import Base
    from app.db.session import get_engine, get_session_factory

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    engine = get_engine()
    Base.metadata.create_all(engine)

    from app.main import create_app

    with TestClient(create_app()) as client:
        assert client.get('/docs').status_code == 404
        assert client.get('/openapi.json').status_code == 404