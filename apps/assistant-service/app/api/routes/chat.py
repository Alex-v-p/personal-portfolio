from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post('/respond', response_model=ChatResponse)
def respond(payload: ChatRequest, session: Session = Depends(get_session)) -> ChatResponse:
    result = ChatService(session).respond(
        message=payload.message,
        conversation_id=payload.conversation_id,
        session_id=payload.session_id,
        page_path=payload.page_path,
    )
    return ChatResponse(**result)
