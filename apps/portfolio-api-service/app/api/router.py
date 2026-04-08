from fastapi import APIRouter

from app.api.routes import admin, contact, health, public

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(public.router, prefix="/public", tags=["public"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
