from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import AdminAssistantKnowledgeRebuildIn, AdminAssistantKnowledgeRebuildOut, AdminAssistantKnowledgeStatusOut
from app.domains.knowledge.sync import KnowledgeSyncService

router = APIRouter()


@router.get('/assistant/knowledge', response_model=AdminAssistantKnowledgeStatusOut)
def get_assistant_knowledge_status(_: CurrentAdminDep, session: SessionDep) -> AdminAssistantKnowledgeStatusOut:
    return AdminAssistantKnowledgeStatusOut(**asdict(KnowledgeSyncService(session).get_status()))


@router.post('/assistant/knowledge/rebuild', response_model=AdminAssistantKnowledgeRebuildOut)
def rebuild_assistant_knowledge(payload: AdminAssistantKnowledgeRebuildIn, _: CurrentAdminDep, session: SessionDep) -> AdminAssistantKnowledgeRebuildOut:
    del payload
    return AdminAssistantKnowledgeRebuildOut(**asdict(KnowledgeSyncService(session).rebuild()))
