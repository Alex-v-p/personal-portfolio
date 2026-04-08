from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()


class ContactMessageIn(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


@router.post('/messages')
def create_contact_message(payload: ContactMessageIn) -> dict:
    return {
        'message': 'Contact endpoint scaffolded.',
        'received': payload.model_dump()
    }
