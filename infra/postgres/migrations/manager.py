from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from infra.postgres.migrations.state import SchemaState, SchemaStatus, inspect_schema_state

logger = logging.getLogger(__name__)


def migrations_root() -> Path:
    return Path(__file__).resolve().parent


def alembic_ini_path() -> Path:
    return migrations_root() / 'alembic.ini'


def script_location() -> str:
    return str(migrations_root())


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _candidate_env_files() -> list[Path]:
    root = repo_root()
    return [root / '.env', root / 'apps' / 'portfolio-api-service' / '.env']


def _read_env_value_from_file(path: Path, key: str) -> str | None:
    if not path.exists():
        return None

    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        current_key, value = line.split('=', 1)
        if current_key.strip() != key:
            continue
        return value.strip().strip('"\'')
    return None


def resolve_database_url(database_url: str | None = None) -> str | None:
    if database_url:
        return database_url

    for key in ('DATABASE_URL', 'PORTFOLIO_API_DB_URL'):
        value = os.getenv(key)
        if value:
            return value

    for env_file in _candidate_env_files():
        for key in ('DATABASE_URL', 'PORTFOLIO_API_DB_URL'):
            value = _read_env_value_from_file(env_file, key)
            if value:
                return value

    return None


def build_alembic_config(*, database_url: str | None = None) -> Config:
    config = Config(str(alembic_ini_path()))
    config.set_main_option('script_location', script_location())
    root = repo_root()
    api_root = root / 'apps' / 'portfolio-api-service'
    config.set_main_option('prepend_sys_path', os.pathsep.join([str(root), str(api_root)]))

    resolved_url = resolve_database_url(database_url)
    if not resolved_url:
        raise RuntimeError(
            'DATABASE_URL must be set before running migrations. '
            'The CLI also accepts PORTFOLIO_API_DB_URL from the repo .env files.'
        )

    config.set_main_option('sqlalchemy.url', resolved_url)
    return config


def ensure_postgres_extensions(*, database_url: str | None = None) -> None:
    resolved_url = resolve_database_url(database_url)
    if not resolved_url or not resolved_url.startswith('postgresql'):
        return

    engine = create_engine(resolved_url, future=True)
    try:
        with engine.begin() as connection:
            connection.exec_driver_sql('CREATE EXTENSION IF NOT EXISTS vector')
    finally:
        engine.dispose()


def get_schema_status(*, database_url: str | None = None) -> SchemaStatus:
    resolved_url = resolve_database_url(database_url)
    if not resolved_url:
        raise RuntimeError(
            'DATABASE_URL must be set before inspecting schema state. '
            'The CLI also accepts PORTFOLIO_API_DB_URL from the repo .env files.'
        )
    return inspect_schema_state(resolved_url)


def stamp_database(*, revision: str = 'head', database_url: str | None = None) -> None:
    command.stamp(build_alembic_config(database_url=database_url), revision)


def upgrade_database(*, revision: str = 'head', database_url: str | None = None) -> SchemaStatus:
    resolved_url = resolve_database_url(database_url)
    if not resolved_url:
        raise RuntimeError(
            'DATABASE_URL must be set before running migrations. '
            'The CLI also accepts PORTFOLIO_API_DB_URL from the repo .env files.'
        )

    ensure_postgres_extensions(database_url=resolved_url)
    schema_status = inspect_schema_state(resolved_url)

    if schema_status.can_auto_stamp:
        logger.info(
            'Existing schema detected without alembic_version. Stamping database at revision %s instead of recreating tables.',
            revision,
        )
        stamp_database(revision=revision, database_url=resolved_url)
        return schema_status

    if schema_status.state == SchemaState.INCOMPATIBLE:
        missing = ', '.join(schema_status.missing_tables[:10])
        if len(schema_status.missing_tables) > 10:
            missing += ', ...'
        raise RuntimeError(
            'Existing database is missing tables required by the managed schema and cannot be auto-stamped. '
            f'Missing tables: {missing}'
        )

    command.upgrade(build_alembic_config(database_url=resolved_url), revision)
    return schema_status


def create_revision(*, message: str, autogenerate: bool = False, database_url: str | None = None) -> None:
    if not message.strip():
        raise RuntimeError('Migration message cannot be empty.')
    command.revision(
        build_alembic_config(database_url=database_url),
        message=message.strip(),
        autogenerate=autogenerate,
    )


def migration_smoke_check() -> None:
    with tempfile.TemporaryDirectory(prefix='portfolio-migration-check-') as temp_dir:
        database_path = Path(temp_dir) / 'migration-check.sqlite3'
        upgrade_database(database_url=f'sqlite:///{database_path}')
        logger.info('Migration smoke check passed against %s', database_path)
