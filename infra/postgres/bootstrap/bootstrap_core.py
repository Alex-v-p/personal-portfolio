from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import AdminUser
from app.db.session import get_session_factory
from infra.postgres.bootstrap.seed_data import seed_database
from infra.postgres.migrations.manager import upgrade_database

logger = logging.getLogger(__name__)


def initialize_database(*, auto_seed: bool = True, recreate_on_drift: bool = False, raise_on_error: bool = False) -> bool:
    try:
        if recreate_on_drift:
            logger.warning(
                'DB_BOOTSTRAP_RECREATE_ON_DRIFT is deprecated and ignored. '
                'Schema changes are now managed through Alembic migrations.'
            )

        upgrade_database()

        if auto_seed:
            session_factory = get_session_factory()
            with session_factory() as session:
                admin_exists = session.execute(select(AdminUser.id).limit(1)).scalar_one_or_none() is not None
                if not admin_exists:
                    seed_database(session)
                else:
                    logger.info('Seed data skipped because the database already contains admin users.')
        return True
    except SQLAlchemyError:
        logger.exception('Failed to initialize database schema through migrations.')
        if raise_on_error:
            raise
        return False
    except Exception:
        logger.exception('Failed to initialize database schema through migrations.')
        if raise_on_error:
            raise
        return False
