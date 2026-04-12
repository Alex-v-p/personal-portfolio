from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.chat import ProviderStatusOut

router = APIRouter()


@router.get('/', response_model=list[ProviderStatusOut])
def list_providers() -> list[ProviderStatusOut]:
    settings = get_settings()
    return [
        ProviderStatusOut(
            backend=settings.provider_backend,
            model=settings.provider_model,
            base_url=settings.provider_base_url,
            configured=settings.provider_backend.strip().lower() != 'mock',
        )
    ]
