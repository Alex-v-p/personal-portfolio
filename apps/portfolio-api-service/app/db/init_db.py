from __future__ import annotations

import logging

from sqlalchemy.exc import SQLAlchemyError

from app.db import Base  # noqa: F401
from app.db.seed_data import seed_database
from app.db.session import get_engine, get_session_factory

logger = logging.getLogger(__name__)


def initialize_database(*, auto_seed: bool = True, raise_on_error: bool = False) -> bool:
    engine = get_engine()
    try:
        if engine.dialect.name == 'postgresql':
            with engine.begin() as connection:
                connection.exec_driver_sql('CREATE EXTENSION IF NOT EXISTS vector')
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
