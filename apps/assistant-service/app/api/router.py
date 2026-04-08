from fastapi import APIRouter

from app.api.routes import chat, conversations, health, providers

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
