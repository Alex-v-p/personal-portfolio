from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.chat.schema import ChatRequest, ChatResponse
from app.core.config import get_settings
from app.domains.chat.service.service import ChatService
from app.services.request_protection import derive_request_identifier, enforce_rate_limit_or_429, ensure_payload_size_within_limit

router = APIRouter()


@router.post('/respond', response_model=ChatResponse)
def respond(payload: ChatRequest, request: Request, session: Session = Depends(get_session)) -> ChatResponse:
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
    result = ChatService(session).respond(
        message=payload.message,
        conversation_id=payload.conversation_id,
        session_id=payload.session_id,
        site_session_id=payload.site_session_id,
        visitor_id=payload.visitor_id,
        page_path=payload.page_path,
        request=request,
    )
    return ChatResponse(**result)
