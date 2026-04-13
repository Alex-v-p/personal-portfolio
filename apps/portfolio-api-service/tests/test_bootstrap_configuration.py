from __future__ import annotations

import pytest

from infra.postgres.bootstrap.bootstrap_database import validate_bootstrap_configuration


def test_validate_bootstrap_configuration_allows_safe_production_mode() -> None:
    validate_bootstrap_configuration(app_env='production', recreate_on_drift=False)


def test_validate_bootstrap_configuration_rejects_destructive_production_mode() -> None:
    with pytest.raises(RuntimeError, match='DB_BOOTSTRAP_RECREATE_ON_DRIFT cannot be enabled'):
        validate_bootstrap_configuration(app_env='production', recreate_on_drift=True)
