from app.core.config import get_settings
from app.domains.providers.client import ProviderClient


def test_health_status_reports_ready_when_provider_is_online(client, monkeypatch) -> None:
    monkeypatch.setattr(ProviderClient, 'check_health', lambda self: (True, 'Ollama is online.'))
    settings = get_settings()
    settings.provider_backend = 'ollama'
    settings.provider_model = 'qwen2.5:3b'

    response = client.get('/api/health/status')

    assert response.status_code == 200
    body = response.json()
    assert body['mode'] == 'ready'
    assert body['providerBackend'] == 'ollama'
    assert body['providerAvailable'] is True


def test_health_status_reports_fallback_when_provider_is_offline(client, monkeypatch) -> None:
    monkeypatch.setattr(ProviderClient, 'check_health', lambda self: (False, 'Could not reach the Ollama instance.'))
    settings = get_settings()
    settings.provider_backend = 'ollama'
    settings.provider_model = 'qwen2.5:3b'

    response = client.get('/api/health/status')

    assert response.status_code == 200
    body = response.json()
    assert body['mode'] == 'fallback'
    assert body['providerAvailable'] is False


def test_health_status_reports_preview_when_mock_mode_is_enabled(client, monkeypatch) -> None:
    monkeypatch.setattr(ProviderClient, 'check_health', lambda self: (True, 'Preview mode is enabled.'))
    settings = get_settings()
    settings.provider_backend = 'mock'
    settings.provider_model = 'mock'

    response = client.get('/api/health/status')

    assert response.status_code == 200
    body = response.json()
    assert body['mode'] == 'preview'
    assert body['providerAvailable'] is True
