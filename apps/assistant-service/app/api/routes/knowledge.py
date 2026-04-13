from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.chat import KnowledgeStatusOut
from app.services.retrieval_service import KnowledgeRetrievalService
from app.services.security import get_current_admin_user

router = APIRouter()


@router.get('/status', response_model=KnowledgeStatusOut)
def knowledge_status(_: dict = Depends(get_current_admin_user), session: Session = Depends(get_session)) -> KnowledgeStatusOut:
    return KnowledgeStatusOut(**KnowledgeRetrievalService(session).get_status())
