from fastapi import APIRouter

from app.api.routes import health
from app.api.routes.admin import router as admin_router
from app.api.routes import contact
from app.api.routes import public
from app.api.routes import events

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(public.router, prefix="/public", tags=["public"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
