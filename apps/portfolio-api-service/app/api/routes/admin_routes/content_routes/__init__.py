from fastapi import APIRouter

from app.api.routes.admin_routes.content_routes import blog, experience, navigation, profile, projects

router = APIRouter()
for module in (projects, blog, experience, navigation, profile):
    router.include_router(module.router)
