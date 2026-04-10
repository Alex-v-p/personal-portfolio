from __future__ import annotations

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
