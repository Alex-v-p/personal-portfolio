from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.api.routes.admin.common import CurrentAdminDep
from app.domains.admin.schema import AdminAsyncTaskStatusOut
from app.services.async_tasks import TaskQueueUnavailable, get_admin_task_queue

router = APIRouter()


@router.get('/tasks/{task_id}', response_model=AdminAsyncTaskStatusOut)
def get_admin_task(task_id: str, _: CurrentAdminDep) -> AdminAsyncTaskStatusOut:
    try:
        task = get_admin_task_queue().get(task_id)
    except TaskQueueUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found.')
    return AdminAsyncTaskStatusOut(
        task_id=task.task_id,
        task_type=task.task_type,
        status=task.status,
        submitted_at=task.submitted_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        error_message=task.error_message,
        result=task.result,
    )
