from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_session
from app.domains.chat.schema import ChatRequest, ChatResponse, ChatTaskAccepted, ChatTaskStatus
from app.domains.chat.service.service import ChatService
from app.services.async_tasks import CHAT_RESPONSE_TASK, TaskQueueUnavailable, get_chat_task_queue
from app.services.request_protection import derive_request_identifier, enforce_rate_limit_or_429, ensure_payload_size_within_limit

router = APIRouter()


@router.post('/respond', response_model=ChatResponse | ChatTaskAccepted)
def respond(payload: ChatRequest, request: Request, session: Session = Depends(get_session)) -> ChatResponse | JSONResponse:
    settings = get_settings()
    ensure_payload_size_within_limit(
        payload,
        max_bytes=settings.chat_max_request_bytes,
        detail='Chat request payload is too large.',
    )
    enforce_rate_limit_or_429(
        scope='chat-respond',
        identifier=derive_request_identifier(request, payload.visitor_id, payload.site_session_id, payload.session_id),
        limit=settings.chat_rate_limit_max_requests,
        window_seconds=settings.chat_rate_limit_window_seconds,
        detail='Too many assistant messages were sent in a short period. Please wait a moment before trying again.',
    )
    task_queue = get_chat_task_queue()
    if task_queue.enabled:
        try:
            conversation_id, resolved_session_id = ChatService(session).ensure_conversation_identity(
                conversation_id=payload.conversation_id,
                session_id=payload.session_id,
            )
            task = task_queue.enqueue(
                CHAT_RESPONSE_TASK,
                {
                    'conversation_id': conversation_id,
                    'session_id': resolved_session_id,
                    'site_session_id': payload.site_session_id,
                    'visitor_id': payload.visitor_id,
                    'page_path': payload.page_path,
                    'locale': payload.locale,
                    'message': payload.message,
                },
            )
            accepted = ChatTaskAccepted(
                task_id=task.task_id,
                conversation_id=conversation_id,
                status=task.status,
                poll_after_ms=task_queue.poll_after_ms,
            )
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=accepted.model_dump(mode='json', by_alias=True))
        except TaskQueueUnavailable:
            pass
    result = ChatService(session).respond(
        message=payload.message,
        conversation_id=payload.conversation_id,
        session_id=payload.session_id,
        site_session_id=payload.site_session_id,
        visitor_id=payload.visitor_id,
        page_path=payload.page_path,
        locale=payload.locale,
        request=request,
    )
    return ChatResponse(**result)


@router.get('/tasks/{task_id}', response_model=ChatTaskStatus)
def get_chat_task_status(task_id: str) -> ChatTaskStatus:
    try:
        task = get_chat_task_queue().get(task_id)
    except TaskQueueUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if task is None:
        raise HTTPException(status_code=404, detail='Chat task not found.')
    result = task.result or {}
    return ChatTaskStatus(
        task_id=task.task_id,
        conversation_id=str(result.get('conversationId') or result.get('conversation_id') or ''),
        status=task.status,
        submitted_at=task.submitted_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        error_message=task.error_message,
        message=result.get('message') if isinstance(result.get('message'), str) else None,
        provider_backend=result.get('providerBackend') if isinstance(result.get('providerBackend'), str) else None,
        citations=result.get('citations') if isinstance(result.get('citations'), list) else [],
    )
