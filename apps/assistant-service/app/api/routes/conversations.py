from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def list_conversations() -> dict:
    return {
        'items': [],
        'message': 'Conversation storage scaffolded.'
    }
