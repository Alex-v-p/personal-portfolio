from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AdminLoginIn(BaseModel):
    email: str
    password: str


@router.post('/auth/login')
def login(payload: AdminLoginIn) -> dict:
    return {
        'message': 'Admin auth scaffolded.',
        'email': payload.email
    }
