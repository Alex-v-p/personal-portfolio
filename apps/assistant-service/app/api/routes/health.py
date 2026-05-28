from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import get_settings
from app.domains.chat.schema import AssistantHealthOut
from app.domains.providers.client import ProviderClient

router = APIRouter()


@router.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok', 'service': 'assistant-service'}


@router.get('/health/status', response_model=AssistantHealthOut)
def health_status() -> AssistantHealthOut:
    settings = get_settings()
    provider_available, detail = ProviderClient().check_health()
    backend = settings.provider_backend.strip().lower()
    if backend == 'mock':
        mode = 'preview'
        provider_available = True
    else:
        mode = 'ready' if provider_available else 'fallback'
    return AssistantHealthOut(
        status='ok',
        mode=mode,
        provider_backend=settings.provider_backend,
        provider_model=settings.provider_model,
        provider_available=provider_available,
        configured=backend != 'mock',
        detail=detail,
        checked_at=datetime.now(timezone.utc).isoformat(),
    )
