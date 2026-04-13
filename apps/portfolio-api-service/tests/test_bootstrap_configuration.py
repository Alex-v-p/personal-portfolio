from __future__ import annotations

import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect, select

from app.core.config import get_settings
from app.db.models import AdminUser
from app.db.session import reset_database_caches, get_session_factory
from infra.postgres.bootstrap.bootstrap_core import initialize_database
from infra.postgres.bootstrap.bootstrap_database import validate_bootstrap_configuration
from infra.postgres.migrations.manager import build_alembic_config, migration_smoke_check, upgrade_database


def test_validate_bootstrap_configuration_allows_safe_production_mode() -> None:
    validate_bootstrap_configuration(app_env='production', recreate_on_drift=False)


def test_validate_bootstrap_configuration_rejects_destructive_production_mode() -> None:
    with pytest.raises(RuntimeError, match='DB_BOOTSTRAP_RECREATE_ON_DRIFT cannot be enabled'):
        validate_bootstrap_configuration(app_env='production', recreate_on_drift=True)


def test_initialize_database_applies_migrations_and_seeds(tmp_path: Path) -> None:
    database_path = tmp_path / 'migrated.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'test-admin-pass'
    os.environ['ADMIN_DISPLAY_NAME'] = 'Test Admin'

    get_settings.cache_clear()
    reset_database_caches()

    assert initialize_database(auto_seed=True, recreate_on_drift=False, raise_on_error=True) is True

    inspector = inspect(create_engine(f'sqlite:///{database_path}', future=True))
    assert 'alembic_version' in inspector.get_table_names()
    assert 'projects' in inspector.get_table_names()

    session_factory = get_session_factory()
    with session_factory() as session:
        admin = session.execute(select(AdminUser).limit(1)).scalar_one_or_none()
        assert admin is not None
        assert admin.email == 'admin@example.com'


def test_migration_smoke_check_runs_against_temp_sqlite() -> None:
    migration_smoke_check()


def test_upgrade_database_stamps_existing_schema_without_recreating_tables(tmp_path: Path) -> None:
    from app.db import models  # noqa: F401
    from app.db.base import Base
    from app.db.session import get_engine

    database_path = tmp_path / 'existing-schema.sqlite3'
    database_url = f'sqlite:///{database_path}'
    os.environ['DATABASE_URL'] = database_url

    get_settings.cache_clear()
    reset_database_caches()

    engine = get_engine()
    Base.metadata.create_all(engine)
    engine.dispose()

    upgrade_database(database_url=database_url)

    inspector = inspect(create_engine(database_url, future=True))
    assert 'alembic_version' in inspector.get_table_names()


def test_build_alembic_config_reads_database_url_from_repo_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from infra.postgres.migrations import manager

    (tmp_path / '.env').write_text('PORTFOLIO_API_DB_URL=sqlite:///from-env.sqlite3\n', encoding='utf-8')
    (tmp_path / 'apps' / 'portfolio-api-service').mkdir(parents=True, exist_ok=True)

    monkeypatch.delenv('DATABASE_URL', raising=False)
    monkeypatch.delenv('PORTFOLIO_API_DB_URL', raising=False)
    monkeypatch.setattr(manager, 'repo_root', lambda: tmp_path)

    config = build_alembic_config()
    assert config.get_main_option('sqlalchemy.url') == 'sqlite:///from-env.sqlite3'
