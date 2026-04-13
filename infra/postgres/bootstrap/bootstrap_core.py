from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum

from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_session_factory
from infra.postgres.bootstrap.seed_data import seed_database
from infra.postgres.migrations.manager import get_schema_status, upgrade_database
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


def run_bootstrap(*, auto_seed: bool = True, seed_mode: str | None = None, recreate_on_drift: bool = False) -> BootstrapResult:
    if recreate_on_drift:
        logger.warning(
            'DB_BOOTSTRAP_RECREATE_ON_DRIFT is deprecated and ignored. '
            'Schema changes are now managed through Alembic migrations.'
        )

    resolved_seed_mode = resolve_seed_mode(auto_seed=auto_seed, seed_mode=seed_mode)
    schema_status_before = get_schema_status()
    upgrade_database()

    seeded = False
    if _should_seed(resolved_seed_mode=resolved_seed_mode, schema_status_before=schema_status_before):
        session_factory = get_session_factory()
        with session_factory() as session:
            seed_database(session)
        seeded = True
        logger.info('Database seed finished using mode=%s.', resolved_seed_mode.value)
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
