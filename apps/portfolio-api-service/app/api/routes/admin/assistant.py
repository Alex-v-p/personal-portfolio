from __future__ import annotations

from dataclasses import asdict
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.db.models import AssistantContextNote
from app.domains.admin.schema import (
    AdminAssistantContextNoteOut,
    AdminAssistantContextNoteUpsertIn,
    AdminAssistantContextNotesListOut,
    AdminAssistantKnowledgeRebuildIn,
    AdminAssistantKnowledgeRebuildOut,
    AdminAssistantKnowledgeStatusOut,
    AdminAsyncTaskAcceptedOut,
    AdminTranslationDraftIn,
    AdminTranslationDraftOut,
)
from app.domains.admin.service.admin_translation_service import AdminTranslationDraftService
from app.domains.knowledge.service.service import KnowledgeSyncService
from app.services.async_tasks import KNOWLEDGE_REBUILD_TASK, TaskQueueUnavailable, get_admin_task_queue

router = APIRouter()


def _map_context_note(note: AssistantContextNote) -> AdminAssistantContextNoteOut:
    return AdminAssistantContextNoteOut(
        id=note.id,
        title=note.title,
        title_nl=note.title_nl,
        content_markdown=note.content_markdown,
        content_markdown_nl=note.content_markdown_nl,
        category=note.category,
        is_active=note.is_active,
        sort_order=note.sort_order,
        created_at=note.created_at.isoformat() if note.created_at else '',
        updated_at=note.updated_at.isoformat() if note.updated_at else '',
    )


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


@router.get('/assistant/context-notes', response_model=AdminAssistantContextNotesListOut)
def list_assistant_context_notes(_: CurrentAdminDep, session: SessionDep) -> AdminAssistantContextNotesListOut:
    notes = session.scalars(
        select(AssistantContextNote).order_by(AssistantContextNote.sort_order.asc(), AssistantContextNote.title.asc())
    ).all()
    return AdminAssistantContextNotesListOut(items=[_map_context_note(note) for note in notes], total=len(notes))


@router.post('/assistant/context-notes', response_model=AdminAssistantContextNoteOut, status_code=status.HTTP_201_CREATED)
def create_assistant_context_note(
    payload: AdminAssistantContextNoteUpsertIn,
    _: CurrentAdminDep,
    session: SessionDep,
) -> AdminAssistantContextNoteOut:
    note = AssistantContextNote(
        title=payload.title.strip(),
        title_nl=_optional_text(payload.title_nl),
        content_markdown=payload.content_markdown.strip(),
        content_markdown_nl=_optional_text(payload.content_markdown_nl),
        category=payload.category.strip() or 'overall_skills',
        is_active=payload.is_active,
        sort_order=payload.sort_order,
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    return _map_context_note(note)


@router.put('/assistant/context-notes/{note_id}', response_model=AdminAssistantContextNoteOut)
def update_assistant_context_note(
    note_id: UUID,
    payload: AdminAssistantContextNoteUpsertIn,
    _: CurrentAdminDep,
    session: SessionDep,
) -> AdminAssistantContextNoteOut:
    note = session.get(AssistantContextNote, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Assistant context note not found.')
    note.title = payload.title.strip()
    note.title_nl = _optional_text(payload.title_nl)
    note.content_markdown = payload.content_markdown.strip()
    note.content_markdown_nl = _optional_text(payload.content_markdown_nl)
    note.category = payload.category.strip() or 'overall_skills'
    note.is_active = payload.is_active
    note.sort_order = payload.sort_order
    session.add(note)
    session.commit()
    session.refresh(note)
    return _map_context_note(note)


@router.delete('/assistant/context-notes/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_assistant_context_note(note_id: UUID, _: CurrentAdminDep, session: SessionDep) -> Response:
    note = session.get(AssistantContextNote, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Assistant context note not found.')
    session.delete(note)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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


@router.post('/assistant/translate-draft', response_model=AdminTranslationDraftOut)
def translate_draft(
    payload: AdminTranslationDraftIn,
    _: CurrentAdminDep,
) -> AdminTranslationDraftOut:
    return AdminTranslationDraftService().generate_draft(payload)
