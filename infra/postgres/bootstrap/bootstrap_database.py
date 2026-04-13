from __future__ import annotations

import logging
import os
import sys
import time

from infra.postgres.bootstrap.bootstrap_core import initialize_database

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def validate_bootstrap_configuration(app_env: str, recreate_on_drift: bool) -> None:
    if app_env.strip().lower() == 'production' and recreate_on_drift:
        raise RuntimeError('DB_BOOTSTRAP_RECREATE_ON_DRIFT cannot be enabled when APP_ENV=production.')


def main() -> int:
    app_env = os.getenv('APP_ENV', 'development')
    auto_seed = _env_bool('DB_BOOTSTRAP_AUTO_SEED', True)
    recreate_on_drift = _env_bool('DB_BOOTSTRAP_RECREATE_ON_DRIFT', True)
    max_retries = _env_int('DB_BOOTSTRAP_MAX_RETRIES', 30)
    retry_delay_seconds = _env_int('DB_BOOTSTRAP_RETRY_DELAY_SECONDS', 2)

    validate_bootstrap_configuration(app_env=app_env, recreate_on_drift=recreate_on_drift)

    for attempt in range(1, max_retries + 1):
        try:
            initialize_database(
                auto_seed=auto_seed,
                recreate_on_drift=recreate_on_drift,
                raise_on_error=True,
            )
            logger.info('Database bootstrap finished successfully.')
            return 0
        except Exception:  # pragma: no cover - retry loop behavior is integration-focused
            logger.exception('Database bootstrap attempt %s/%s failed.', attempt, max_retries)
            if attempt == max_retries:
                logger.error('Database bootstrap exhausted all retries.')
                return 1
            time.sleep(retry_delay_seconds)

    return 1


if __name__ == '__main__':
    sys.exit(main())
