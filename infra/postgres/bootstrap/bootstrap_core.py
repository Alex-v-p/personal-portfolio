from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.db.models import AdminUser, Project
from app.db.session import get_session_factory
from infra.postgres.bootstrap.seed_data import seed_database, sync_admin_user
from infra.postgres.migrations.manager import get_schema_status, recreate_schema, upgrade_database
from infra.postgres.migrations.state import SchemaState, SchemaStatus

logger = logging.getLogger(__name__)


class SeedMode(StrEnum):
    NEVER = 'never'
    IF_EMPTY = 'if-empty'
    ALWAYS = 'always'


@dataclass(frozen=True)
class BootstrapResult:
    schema_status_before: SchemaStatus
    seed_mode: SeedMode
    seeded: bool


def resolve_seed_mode(*, auto_seed: bool = True, seed_mode: str | None = None) -> SeedMode:
    if seed_mode is not None:
        normalized = seed_mode.strip().lower()
        for candidate in SeedMode:
            if candidate.value == normalized:
                return candidate
        raise RuntimeError(f'Unsupported DB_BOOTSTRAP_SEED_MODE: {seed_mode}')

    return SeedMode.IF_EMPTY if auto_seed else SeedMode.NEVER


def _should_seed(*, resolved_seed_mode: SeedMode, schema_status_before: SchemaStatus) -> bool:
    if resolved_seed_mode == SeedMode.NEVER:
        return False
    if resolved_seed_mode == SeedMode.ALWAYS:
        return True
    return schema_status_before.state == SchemaState.EMPTY


def _should_sync_admin(*, resolved_seed_mode: SeedMode, schema_status_before: SchemaStatus) -> bool:
    return resolved_seed_mode != SeedMode.NEVER and schema_status_before.state == SchemaState.MANAGED


def _database_has_seed_content() -> bool:
    session_factory = get_session_factory()
    with session_factory() as session:
        return (
            session.execute(select(Project.id).limit(1)).scalar_one_or_none() is not None
            or session.execute(select(AdminUser.id).limit(1)).scalar_one_or_none() is not None
        )


def run_bootstrap(*, auto_seed: bool = True, seed_mode: str | None = None, recreate_on_drift: bool = False) -> BootstrapResult:
    if recreate_on_drift:
        logger.warning(
            'DB_BOOTSTRAP_RECREATE_ON_DRIFT is deprecated and ignored. '
            'Schema changes are now managed through Alembic migrations.'
        )

    resolved_seed_mode = resolve_seed_mode(auto_seed=auto_seed, seed_mode=seed_mode)
    schema_status_before = get_schema_status()

    if recreate_on_drift and schema_status_before.state == SchemaState.INCOMPATIBLE:
        logger.warning('Existing schema is incompatible with the managed migration baseline. Recreating schema because recreate_on_drift=True.')
        recreate_schema()
        schema_status_before = SchemaStatus(
            state=SchemaState.EMPTY,
            table_names=(),
            has_alembic_version=False,
        )

    upgrade_database()

    seeded = False
    if _should_seed(resolved_seed_mode=resolved_seed_mode, schema_status_before=schema_status_before):
        session_factory = get_session_factory()
        with session_factory() as session:
            seed_database(session)
        seeded = True
        logger.info('Database seed finished using mode=%s.', resolved_seed_mode.value)
    elif _should_sync_admin(resolved_seed_mode=resolved_seed_mode, schema_status_before=schema_status_before) and _database_has_seed_content():
        session_factory = get_session_factory()
        with session_factory() as session:
            sync_admin_user(session)
        logger.info('Admin bootstrap sync finished using mode=%s.', resolved_seed_mode.value)
    else:
        logger.info(
            'Database seed skipped using mode=%s (schema state before migration: %s).',
            resolved_seed_mode.value,
            schema_status_before.state,
        )

    return BootstrapResult(
        schema_status_before=schema_status_before,
        seed_mode=resolved_seed_mode,
        seeded=seeded,
    )


def initialize_database(*, auto_seed: bool = True, seed_mode: str | None = None, recreate_on_drift: bool = False, raise_on_error: bool = False) -> bool:
    try:
        run_bootstrap(auto_seed=auto_seed, seed_mode=seed_mode, recreate_on_drift=recreate_on_drift)
        return True
    except SQLAlchemyError:
        logger.exception('Failed to initialize database through migrations/bootstrap.')
        if raise_on_error:
            raise
        return False
    except Exception:
        logger.exception('Failed to initialize database through migrations/bootstrap.')
        if raise_on_error:
            raise
        return False
