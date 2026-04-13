from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True)
def _reset_rate_limit_state() -> None:
    os.environ.setdefault('REDIS_URL', 'memory://')
    from app.services.rate_limit import reset_rate_limit_state

    reset_rate_limit_state()
    yield
    reset_rate_limit_state()
