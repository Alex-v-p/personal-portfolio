from __future__ import annotations

from fastapi.testclient import TestClient


ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'test-admin-pass'


def _admin_token(client: TestClient) -> str:
    response = client.post('/api/admin/auth/login', json={'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD})
    assert response.status_code == 200
    return response.json()['accessToken']


def test_admin_login_returns_bearer_token(client: TestClient) -> None:
    response = client.post('/api/admin/auth/login', json={'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD})
    assert response.status_code == 200
    body = response.json()
    assert body['tokenType'] == 'bearer'
    assert body['user']['email'] == ADMIN_EMAIL


def test_admin_endpoints_require_auth(client: TestClient) -> None:
    response = client.get('/api/admin/projects')
    assert response.status_code == 401


def test_admin_can_create_update_and_delete_project(client: TestClient) -> None:
    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    reference = client.get('/api/admin/reference-data', headers=headers)
    assert reference.status_code == 200
    skill_id = reference.json()['skills'][0]['id']

    create_response = client.post(
        '/api/admin/projects',
        headers=headers,
        json={
            'title': 'Admin created project',
            'teaser': 'A project created from the admin CMS.',
            'summary': 'CMS project summary',
            'descriptionMarkdown': '## CMS body',
            'coverImageFileId': None,
            'githubUrl': 'https://github.com/shuzu/admin-created-project',
            'githubRepoOwner': 'shuzu',
            'githubRepoName': 'admin-created-project',
            'demoUrl': 'https://example.com/demo',
            'companyName': 'Independent',
            'startedOn': '2026-01-01',
            'endedOn': None,
            'durationLabel': '2 weeks',
            'status': 'In progress',
            'state': 'published',
            'isFeatured': False,
            'sortOrder': 88,
            'publishedAt': '2026-01-15T09:00:00+00:00',
            'skillIds': [skill_id],
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created['slug'] == 'admin-created-project'
    assert created['skillIds'] == [skill_id]

    update_response = client.put(
        f"/api/admin/projects/{created['id']}",
        headers=headers,
        json={
            'slug': 'admin-created-project-updated',
            'title': 'Admin created project updated',
            'teaser': 'Updated teaser',
            'summary': 'Updated summary',
            'descriptionMarkdown': 'Updated markdown',
            'coverImageFileId': None,
            'githubUrl': 'https://github.com/shuzu/admin-created-project-updated',
            'githubRepoOwner': 'shuzu',
            'githubRepoName': 'admin-created-project-updated',
            'demoUrl': 'https://example.com/updated-demo',
            'companyName': 'Independent',
            'startedOn': '2026-01-01',
            'endedOn': '2026-01-20',
            'durationLabel': '3 weeks',
            'status': 'Completed',
            'state': 'completed',
            'isFeatured': True,
            'sortOrder': 77,
            'publishedAt': '2026-01-20T09:00:00+00:00',
            'skillIds': [skill_id],
        },
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated['slug'] == 'admin-created-project-updated'
    assert updated['isFeatured'] is True

    delete_response = client.delete(f"/api/admin/projects/{created['id']}", headers=headers)
    assert delete_response.status_code == 204


def test_admin_can_manage_blog_posts(client: TestClient) -> None:
    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    create_response = client.post(
        '/api/admin/blog-posts',
        headers=headers,
        json={
            'title': 'CMS launch notes',
            'excerpt': 'Blog post created from the admin panel.',
            'contentMarkdown': '# Launch\n\nNew post body',
            'coverImageFileId': None,
            'coverImageAlt': 'Launch article cover',
            'readingTimeMinutes': 4,
            'status': 'draft',
            'isFeatured': False,
            'publishedAt': None,
            'seoTitle': 'CMS launch notes',
            'seoDescription': 'Admin-created post',
            'tagNames': ['CMS', 'Angular'],
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created['slug'] == 'cms-launch-notes'
    assert 'CMS' in created['tagNames']

    update_response = client.put(
        f"/api/admin/blog-posts/{created['id']}",
        headers=headers,
        json={
            'slug': 'cms-launch-notes-published',
            'title': 'CMS launch notes published',
            'excerpt': 'Published excerpt',
            'contentMarkdown': '# Published',
            'coverImageFileId': None,
            'coverImageAlt': 'Published article cover',
            'readingTimeMinutes': 5,
            'status': 'published',
            'isFeatured': True,
            'publishedAt': '2026-02-01T10:00:00+00:00',
            'seoTitle': 'Published CMS launch notes',
            'seoDescription': 'Published admin-created post',
            'tagNames': ['CMS', 'FastAPI'],
        },
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated['status'] == 'published'
    assert updated['isFeatured'] is True
    assert 'FastAPI' in updated['tagNames']


def test_admin_can_update_profile(client: TestClient) -> None:
    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    current_profile = client.get('/api/admin/profile', headers=headers)
    assert current_profile.status_code == 200
    profile = current_profile.json()

    update_response = client.put(
        '/api/admin/profile',
        headers=headers,
        json={
            'firstName': 'Alex',
            'lastName': 'van Poppel',
            'headline': 'Software Engineer & CMS owner',
            'shortIntro': 'Updated intro from the admin profile editor.',
            'longBio': 'Longer bio updated through the admin CMS.',
            'location': 'Belgium',
            'email': 'hello@shuzu.dev',
            'phone': profile['phone'],
            'avatarFileId': profile['avatarFileId'],
            'heroImageFileId': profile['heroImageFileId'],
            'resumeFileId': profile['resumeFileId'],
            'ctaPrimaryLabel': 'View resume',
            'ctaPrimaryUrl': 'media://resume',
            'ctaSecondaryLabel': 'Email me',
            'ctaSecondaryUrl': 'mailto:hello@shuzu.dev',
            'isPublic': True,
            'socialLinks': [
                {
                    'id': profile['socialLinks'][0]['id'],
                    'platform': profile['socialLinks'][0]['platform'],
                    'label': profile['socialLinks'][0]['label'],
                    'url': profile['socialLinks'][0]['url'],
                    'iconKey': profile['socialLinks'][0]['iconKey'],
                    'sortOrder': profile['socialLinks'][0]['sortOrder'],
                    'isVisible': True,
                },
                {
                    'platform': 'portfolio',
                    'label': 'Portfolio',
                    'url': 'https://example.com',
                    'iconKey': 'globe',
                    'sortOrder': 20,
                    'isVisible': True,
                },
            ],
        },
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated['headline'] == 'Software Engineer & CMS owner'
    assert len(updated['socialLinks']) == 2


def test_admin_can_read_and_mark_contact_messages(client: TestClient) -> None:
    client.post(
        '/api/contact/messages',
        json={
            'name': 'Casey',
            'email': 'casey@example.com',
            'subject': 'Hello',
            'message': 'Testing admin inbox message',
            'sourcePage': '/contact',
        },
    )

    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/admin/contact-messages', headers=headers)
    assert response.status_code == 200
    message = response.json()['items'][0]
    assert message['email'] == 'casey@example.com'

    mark_response = client.patch(
        f"/api/admin/contact-messages/{message['id']}",
        headers=headers,
        json={'isRead': True},
    )
    assert mark_response.status_code == 200
    assert mark_response.json()['isRead'] is True
