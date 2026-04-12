from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.chat import KnowledgeStatusOut
from app.services.retrieval_service import KnowledgeRetrievalService

router = APIRouter()


@router.get('/status', response_model=KnowledgeStatusOut)
def knowledge_status(session: Session = Depends(get_session)) -> KnowledgeStatusOut:
    return KnowledgeStatusOut(**KnowledgeRetrievalService(session).get_status())
