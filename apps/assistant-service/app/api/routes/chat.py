from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


@router.post('/respond')
def respond(payload: ChatRequest) -> dict:
    return {
        'message': 'Assistant chat scaffolded.',
        'received': payload.model_dump()
    }
