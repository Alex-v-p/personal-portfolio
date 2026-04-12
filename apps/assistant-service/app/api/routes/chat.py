from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post('/respond', response_model=ChatResponse)
def respond(payload: ChatRequest, request: Request, session: Session = Depends(get_session)) -> ChatResponse:
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
