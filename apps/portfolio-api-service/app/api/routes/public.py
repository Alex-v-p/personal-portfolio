from fastapi import APIRouter

router = APIRouter()


@router.get('/profile')
def get_profile() -> dict:
    return {
        'message': 'Profile endpoint scaffolded.',
        'next_step': 'Replace this stub with real profile content.'
    }


@router.get('/projects')
def list_projects() -> dict:
    return {
        'items': [],
        'message': 'Projects endpoint scaffolded.'
    }


@router.get('/experience')
def list_experience() -> dict:
    return {
        'items': [],
        'message': 'Experience endpoint scaffolded.'
    }
