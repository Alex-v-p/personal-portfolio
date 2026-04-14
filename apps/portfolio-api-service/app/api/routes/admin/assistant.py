from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import (
    AdminAssistantKnowledgeRebuildIn,
    AdminAssistantKnowledgeRebuildOut,
    AdminAssistantKnowledgeStatusOut,
    AdminAsyncTaskAcceptedOut,
)
from app.domains.knowledge.service.service import KnowledgeSyncService
from app.services.async_tasks import KNOWLEDGE_REBUILD_TASK, TaskQueueUnavailable, get_admin_task_queue

router = APIRouter()


@router.get('/assistant/knowledge', response_model=AdminAssistantKnowledgeStatusOut)
def get_assistant_knowledge_status(_: CurrentAdminDep, session: SessionDep) -> AdminAssistantKnowledgeStatusOut:
    return AdminAssistantKnowledgeStatusOut(**asdict(KnowledgeSyncService(session).get_status()))


@router.post('/assistant/knowledge/rebuild', response_model=AdminAssistantKnowledgeRebuildOut | AdminAsyncTaskAcceptedOut)
def rebuild_assistant_knowledge(
    payload: AdminAssistantKnowledgeRebuildIn,
    _: CurrentAdminDep,
    session: SessionDep,
) -> AdminAssistantKnowledgeRebuildOut | JSONResponse:
    del payload
    task_queue = get_admin_task_queue()
    if task_queue.enabled:
        try:
            task = task_queue.enqueue(KNOWLEDGE_REBUILD_TASK, {})
            accepted = AdminAsyncTaskAcceptedOut(
                task_id=task.task_id,
                task_type=KNOWLEDGE_REBUILD_TASK,
                status=task.status,
                poll_after_ms=task_queue.poll_after_ms,
            )
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=accepted.model_dump(mode='json', by_alias=True))
        except TaskQueueUnavailable:
            pass
    return AdminAssistantKnowledgeRebuildOut(**asdict(KnowledgeSyncService(session).rebuild()))
