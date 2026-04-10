from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.db.init_db import initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    if settings.db_auto_create:
        initialize_database(auto_seed=settings.db_auto_seed, raise_on_error=not settings.db_startup_graceful)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
        docs_url='/docs',
        openapi_url='/openapi.json',
        redoc_url=None,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins_list,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.include_router(api_router)

    @app.get('/')
    def root() -> dict[str, str]:
        return {'message': 'Portfolio API is running.'}

    return app


app = create_app()
