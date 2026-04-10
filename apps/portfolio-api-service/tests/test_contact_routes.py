from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.api.routes import contact
from app.main import app
from app.services.contact_message_store import ContactMessageStore

client = TestClient(app)


def test_create_contact_message_returns_created_payload(tmp_path: Path) -> None:
    storage_file = tmp_path / 'contact_messages.json'
    original_store = contact.store
    contact.store = ContactMessageStore(storage_file=storage_file)

    try:
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
    finally:
        contact.store = original_store

    assert response.status_code == 201
    body = response.json()
    assert body['message'] == 'Contact message saved.'
    assert body['item']['subject'] == 'Internship question'
    assert body['item']['isRead'] is False
