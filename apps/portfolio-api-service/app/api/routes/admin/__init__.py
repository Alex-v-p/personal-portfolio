from fastapi import APIRouter, Depends

from app.api.routes.admin import activity, assistant, auth, content, media, overview, stats, taxonomy, tasks, users
from app.domains.github.sync import GithubStatsSyncService as GithubStatsSyncService
from app.services.security import require_admin_csrf

router = APIRouter()
for module in (auth, overview, media, taxonomy, content, stats, users, activity, assistant, tasks):
    router.include_router(module.router, dependencies=[Depends(require_admin_csrf)])

__all__ = ['router', 'GithubStatsSyncService']
