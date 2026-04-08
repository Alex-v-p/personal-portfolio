from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def list_providers() -> dict:
    return {
        'items': [],
        'message': 'Provider orchestration scaffolded.'
    }
