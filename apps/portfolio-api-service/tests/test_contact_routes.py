from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient


def test_create_contact_message_returns_created_payload(client: TestClient) -> None:
    response = client.post(
        '/api/contact/messages',
        json={
            'name': 'Alex',
            'email': 'alex@example.com',
            'subject': 'Internship question',
            'message': 'I would like to discuss an internship opportunity and your current availability.',
            'sourcePage': '/contact',
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body['message'] == 'Contact message saved.'
    assert body['item']['subject'] == 'Internship question'
    assert body['item']['isRead'] is False



def test_contact_message_honeypot_field_is_rejected(client: TestClient) -> None:
    response = client.post(
        '/api/contact/messages',
        json={
            'name': 'Alex',
            'email': 'alex@example.com',
            'subject': 'Internship question',
            'message': 'I would like to discuss an internship opportunity and your current availability.',
            'sourcePage': '/contact',
            'website': 'https://spam.example',
        },
    )

    assert response.status_code == 400
    assert response.json()['detail'] == 'Spam protection triggered.'


def test_contact_message_is_rate_limited(tmp_path: Path) -> None:
    import os

    from app.core.config import get_settings
    from app.db.session import reset_database_caches
    from app.services.rate_limit import reset_rate_limit_state
    from infra.postgres.bootstrap.bootstrap_core import initialize_database

    database_path = tmp_path / 'portfolio-contact-rate.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['MEDIA_PUBLIC_BASE_URL'] = 'http://media.example.test'
    os.environ['REDIS_URL'] = 'memory://'
    os.environ['CONTACT_RATE_LIMIT_MAX_REQUESTS'] = '1'
    os.environ['CONTACT_RATE_LIMIT_WINDOW_SECONDS'] = '60'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'test-admin-pass'
    os.environ['ADMIN_DISPLAY_NAME'] = 'Test Admin'
    get_settings.cache_clear()
    reset_database_caches()
    reset_rate_limit_state()
    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

    from app.main import create_app

    with TestClient(create_app()) as rate_limited_client:
        payload = {
            'name': 'Alex',
            'email': 'alex@example.com',
            'subject': 'Internship question',
            'message': 'I would like to discuss an internship opportunity and your current availability.',
            'sourcePage': '/contact',
            'visitorId': 'visitor-1',
        }
        first = rate_limited_client.post('/api/contact/messages', json=payload)
        second = rate_limited_client.post('/api/contact/messages', json=payload)

    assert first.status_code == 201
    assert second.status_code == 429
    assert second.json()['detail'] == 'Too many contact form submissions. Please try again later.'
