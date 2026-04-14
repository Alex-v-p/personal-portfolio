from fastapi import APIRouter

from app.api.routes.admin import activity, assistant, auth, content, media, overview, stats, taxonomy, tasks, users

router = APIRouter()
for module in (auth, overview, media, taxonomy, content, stats, users, activity, assistant, tasks):
    router.include_router(module.router)
