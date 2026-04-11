from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.sqltypes import Uuid

from app.db import Base  # noqa: F401
from infra.postgres.bootstrap.seed_data import seed_database
from app.db.session import get_engine, get_session_factory

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SchemaDrift:
    table_name: str
    column_name: str
    reason: str


def _is_uuid_compatible_type(*, dialect_name: str, database_type: str) -> bool:
    lowered = database_type.lower()
    if 'uuid' in lowered:
        return True
    if dialect_name == 'sqlite' and lowered.startswith('char(32'):
        return True
    return False


def _detect_schema_drift(engine) -> list[SchemaDrift]:
    inspector = inspect(engine)
    drifts: list[SchemaDrift] = []

    for table_name, table in Base.metadata.tables.items():
        if not inspector.has_table(table_name):
            drifts.append(SchemaDrift(table_name=table_name, column_name='*', reason='missing table'))
            continue

        database_columns = {column['name']: column for column in inspector.get_columns(table_name)}
        for model_column in table.columns:
            reflected = database_columns.get(model_column.name)
            if reflected is None:
                drifts.append(SchemaDrift(table_name=table_name, column_name=model_column.name, reason='missing column'))
                continue

            if isinstance(model_column.type, Uuid):
                database_type = str(reflected['type'])
                if not _is_uuid_compatible_type(dialect_name=engine.dialect.name, database_type=database_type):
                    drifts.append(
                        SchemaDrift(
                            table_name=table_name,
                            column_name=model_column.name,
                            reason=f'expected UUID-compatible type, found {database_type}',
                        )
                    )

    return drifts


def initialize_database(*, auto_seed: bool = True, recreate_on_drift: bool = True, raise_on_error: bool = False) -> bool:
    engine = get_engine()
    try:
        if engine.dialect.name == 'postgresql':
            with engine.begin() as connection:
                connection.exec_driver_sql('CREATE EXTENSION IF NOT EXISTS vector')

        if recreate_on_drift:
            drifts = _detect_schema_drift(engine)
            if drifts:
                logger.warning('Schema drift detected. Recreating database schema. Drift count: %s', len(drifts))
                for drift in drifts[:20]:
                    logger.warning('%s.%s -> %s', drift.table_name, drift.column_name, drift.reason)
                Base.metadata.drop_all(bind=engine)

        Base.metadata.create_all(bind=engine)
        if auto_seed:
            session_factory = get_session_factory()
            with session_factory() as session:
                seed_database(session)
        return True
    except SQLAlchemyError:
        logger.exception('Failed to initialize database schema.')
        if raise_on_error:
            raise
        return False
    except Exception:
        logger.exception('Failed to initialize database schema.')
        if raise_on_error:
            raise
        return False
