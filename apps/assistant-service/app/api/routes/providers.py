from fastapi import APIRouter, Depends

from app.core.config import get_settings
from app.schemas.chat import ProviderStatusOut
from app.services.security import get_current_admin_user

router = APIRouter()


@router.get('/', response_model=list[ProviderStatusOut])
def list_providers(_: dict = Depends(get_current_admin_user)) -> list[ProviderStatusOut]:
    settings = get_settings()
    return [
        ProviderStatusOut(
            backend=settings.provider_backend,
            model=settings.provider_model,
            base_url=settings.provider_base_url,
            configured=settings.provider_backend.strip().lower() != 'mock',
        )
    ]
