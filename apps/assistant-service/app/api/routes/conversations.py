from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.domains.chat.schema import ChatMessageOut, ConversationOut, ConversationsListOut
from app.domains.chat.service.service import ChatService
from app.services.security import get_current_admin_user

router = APIRouter()


@router.get('/', response_model=ConversationsListOut)
def list_conversations(_: dict = Depends(get_current_admin_user), session: Session = Depends(get_session)) -> ConversationsListOut:
    items = [
        ConversationOut(
            id=str(item.id),
            session_id=item.session_id,
            started_at=item.started_at.isoformat(),
            last_message_at=item.last_message_at.isoformat(),
            messages=[
                ChatMessageOut(role=message.role.value, text=message.message_text, created_at=message.created_at.isoformat())
                for message in sorted(item.messages, key=lambda row: row.created_at)
            ],
        )
        for item in ChatService(session).list_conversations()
    ]
    return ConversationsListOut(items=items, total=len(items))


@router.get('/{conversation_id}', response_model=ConversationOut)
def get_conversation(
    conversation_id: str,
    _: dict = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
) -> ConversationOut:
    conversation = ChatService(session).get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail='Conversation not found.')
    return ConversationOut(
        id=str(conversation.id),
        session_id=conversation.session_id,
        started_at=conversation.started_at.isoformat(),
        last_message_at=conversation.last_message_at.isoformat(),
        messages=[
            ChatMessageOut(role=message.role.value, text=message.message_text, created_at=message.created_at.isoformat())
            for message in sorted(conversation.messages, key=lambda row: row.created_at)
        ],
    )
