from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pyotp
from fastapi.testclient import TestClient


ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'test-admin-pass'


def _login_admin(client: TestClient):
    response = client.post('/api/admin/auth/login', json={'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD})
    assert response.status_code == 200
    return response


def _admin_headers(client: TestClient) -> dict[str, str]:
    response = _login_admin(client)
    body = response.json()
    csrf_headers = {'X-Portfolio-CSRF': body['csrfToken']}

    if body.get('mfaSetupRequired'):
        setup = client.post('/api/admin/auth/mfa/setup', headers=csrf_headers)
        assert setup.status_code == 200
        setup_body = setup.json()
        code = pyotp.TOTP(setup_body['manualEntryKey']).now()
        confirm = client.post('/api/admin/auth/mfa/setup/confirm', headers=csrf_headers, json={'code': code})
        assert confirm.status_code == 200
        return {'X-Portfolio-CSRF': confirm.json()['session']['csrfToken']}

    return {'X-Portfolio-CSRF': body['csrfToken']}


def test_public_user_journey_can_browse_content_contact_and_track_activity(client: TestClient) -> None:
    home = client.get('/api/public/home')
    assert home.status_code == 200
    assert home.json()['featuredProjects']
    assert home.json()['featuredBlogPosts']

    project_slug = home.json()['featuredProjects'][0]['slug']
    project_detail = client.get(f'/api/public/projects/{project_slug}')
    assert project_detail.status_code == 200

    blog_slug = home.json()['featuredBlogPosts'][0]['slug']
    blog_detail = client.get(f'/api/public/blog-posts/{blog_slug}')
    assert blog_detail.status_code == 200

    contact = client.post(
        '/api/contact/messages',
        json={
            'name': 'Alex',
            'email': 'alex@example.com',
            'subject': 'Phase 4 test message',
            'message': 'This confirms the public contact submission flow still works end to end.',
            'sourcePage': '/contact',
            'visitorId': 'visitor-phase4',
            'sessionId': 'session-phase4',
            'website': '',
        },
    )
    assert contact.status_code == 201
    assert contact.json()['item']['sourcePage'] == '/contact'

    event = client.post(
        '/api/events',
        json={
            'eventType': 'page_view',
            'pagePath': f'/projects/{project_slug}',
            'visitorId': 'visitor-phase4',
            'sessionId': 'session-phase4',
            'metadata': {'origin': 'phase4-test'},
        },
    )
    assert event.status_code == 201
    assert event.json()['message'] == 'Site event stored.'


def test_admin_publish_workflow_controls_public_visibility(client: TestClient) -> None:
    headers = _admin_headers(client)
    reference = client.get('/api/admin/reference-data', headers=headers)
    assert reference.status_code == 200
    skill_id = reference.json()['skills'][0]['id']

    create = client.post(
        '/api/admin/projects',
        headers=headers,
        json={
            'title': 'Phase 4 hidden project',
            'teaser': 'Should start hidden.',
            'summary': 'Hidden summary',
            'descriptionMarkdown': 'Hidden body',
            'coverImageFileId': None,
            'githubUrl': None,
            'githubRepoOwner': None,
            'githubRepoName': None,
            'demoUrl': None,
            'companyName': 'Independent',
            'startedOn': '2026-01-01',
            'endedOn': None,
            'durationLabel': '1 week',
            'status': 'Preview',
            'state': 'completed',
            'isFeatured': False,
            'sortOrder': 150,
            'publishedAt': (datetime.now(UTC) + timedelta(days=7)).isoformat(),
            'skillIds': [skill_id],
        },
    )
    assert create.status_code == 201
    created = create.json()

    hidden_listing = client.get('/api/public/projects')
    assert created['slug'] not in {item['slug'] for item in hidden_listing.json()['items']}
    assert client.get(f"/api/public/projects/{created['slug']}").status_code == 404

    publish = client.put(
        f"/api/admin/projects/{created['id']}",
        headers=headers,
        json={
            'slug': created['slug'],
            'title': 'Phase 4 hidden project',
            'teaser': 'Now public.',
            'summary': 'Published summary',
            'descriptionMarkdown': 'Published body',
            'coverImageFileId': None,
            'githubUrl': None,
            'githubRepoOwner': None,
            'githubRepoName': None,
            'demoUrl': None,
            'companyName': 'Independent',
            'startedOn': '2026-01-01',
            'endedOn': None,
            'durationLabel': '1 week',
            'status': 'Live',
            'state': 'published',
            'isFeatured': True,
            'sortOrder': 25,
            'publishedAt': (datetime.now(UTC) - timedelta(days=1)).isoformat(),
            'skillIds': [skill_id],
        },
    )
    assert publish.status_code == 200

    public_detail = client.get(f"/api/public/projects/{created['slug']}")
    assert public_detail.status_code == 200
    assert public_detail.json()['state'] == 'published'
