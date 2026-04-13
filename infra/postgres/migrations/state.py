from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from sqlalchemy import create_engine, inspect


class SchemaState(StrEnum):
    EMPTY = 'empty'
    MANAGED = 'managed'
    ADOPTABLE = 'adoptable'
    INCOMPATIBLE = 'incompatible'


@dataclass(frozen=True)
class SchemaStatus:
    state: SchemaState
    table_names: tuple[str, ...]
    has_alembic_version: bool
    missing_tables: tuple[str, ...] = ()

    @property
    def is_empty(self) -> bool:
        return self.state == SchemaState.EMPTY

    @property
    def is_managed(self) -> bool:
        return self.state == SchemaState.MANAGED

    @property
    def can_auto_stamp(self) -> bool:
        return self.state == SchemaState.ADOPTABLE


def expected_table_names() -> set[str]:
    from app.db import models  # noqa: F401
    from app.db.base import Base

    return set(Base.metadata.tables.keys())


def inspect_schema_state(database_url: str) -> SchemaStatus:
    engine = create_engine(database_url, future=True)
    try:
        table_names = set(inspect(engine).get_table_names())
    finally:
        engine.dispose()

    ordered_table_names = tuple(sorted(table_names))
    has_alembic_version = 'alembic_version' in table_names

    if not table_names:
        return SchemaStatus(
            state=SchemaState.EMPTY,
            table_names=ordered_table_names,
            has_alembic_version=False,
        )

    if has_alembic_version:
        return SchemaStatus(
            state=SchemaState.MANAGED,
            table_names=ordered_table_names,
            has_alembic_version=True,
        )

    missing_tables = tuple(sorted(expected_table_names() - table_names))
    if missing_tables:
        return SchemaStatus(
            state=SchemaState.INCOMPATIBLE,
            table_names=ordered_table_names,
            has_alembic_version=False,
            missing_tables=missing_tables,
        )

    return SchemaStatus(
        state=SchemaState.ADOPTABLE,
        table_names=ordered_table_names,
        has_alembic_version=False,
    )
