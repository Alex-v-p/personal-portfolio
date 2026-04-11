from __future__ import annotations

from functools import lru_cache
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def _engine_kwargs(database_url: str) -> dict:
    if database_url.startswith('sqlite'):
        return {'connect_args': {'check_same_thread': False}}
    return {}


@lru_cache
def get_engine():
    settings = get_settings()
    return create_engine(settings.database_url, future=True, **_engine_kwargs(settings.database_url))


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def reset_database_caches() -> None:
    get_engine.cache_clear()
    get_session_factory.cache_clear()
