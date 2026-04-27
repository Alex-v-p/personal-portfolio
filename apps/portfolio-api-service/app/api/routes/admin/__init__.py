from fastapi import APIRouter, Depends

from app.api.routes.admin import activity, assistant, auth, backup, content, media, overview, stats, taxonomy, tasks, users
from app.domains.github.sync import GithubStatsSyncService as GithubStatsSyncService
from app.services.security import require_admin_csrf

router = APIRouter()
router.include_router(auth.router, dependencies=[Depends(require_admin_csrf)])
for module in (overview, media, taxonomy, content, stats, users, activity, assistant, backup, tasks):
    router.include_router(module.router, dependencies=[Depends(require_admin_csrf)])

__all__ = ['router', 'GithubStatsSyncService']
