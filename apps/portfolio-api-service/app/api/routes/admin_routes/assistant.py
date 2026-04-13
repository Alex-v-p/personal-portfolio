from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.schemas.admin import AdminAssistantKnowledgeRebuildIn, AdminAssistantKnowledgeRebuildOut, AdminAssistantKnowledgeStatusOut
from app.services.knowledge_sync import KnowledgeSyncService

router = APIRouter()


@router.get('/assistant/knowledge', response_model=AdminAssistantKnowledgeStatusOut)
def get_assistant_knowledge_status(_: CurrentAdminDep, session: SessionDep) -> AdminAssistantKnowledgeStatusOut:
    return AdminAssistantKnowledgeStatusOut(**asdict(KnowledgeSyncService(session).get_status()))


@router.post('/assistant/knowledge/rebuild', response_model=AdminAssistantKnowledgeRebuildOut)
def rebuild_assistant_knowledge(payload: AdminAssistantKnowledgeRebuildIn, _: CurrentAdminDep, session: SessionDep) -> AdminAssistantKnowledgeRebuildOut:
    del payload
    return AdminAssistantKnowledgeRebuildOut(**asdict(KnowledgeSyncService(session).rebuild()))
