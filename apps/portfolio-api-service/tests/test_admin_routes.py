from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.github.sync import SyncedGithubContributionDay, SyncedGithubSnapshot


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

    first_tag_response = client.post(
        '/api/admin/blog-tags',
        headers=headers,
        json={'name': 'Admin CMS', 'slug': 'admin-cms'},
    )
    assert first_tag_response.status_code == 201
    first_tag_id = first_tag_response.json()['id']

    second_tag_response = client.post(
        '/api/admin/blog-tags',
        headers=headers,
        json={'name': 'Admin Angular', 'slug': 'admin-angular'},
    )
    assert second_tag_response.status_code == 201
    second_tag_id = second_tag_response.json()['id']

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
            'tagIds': [first_tag_id, second_tag_id],
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created['slug'] == 'cms-launch-notes'
    assert 'Admin CMS' in created['tagNames']
    assert first_tag_id in created['tagIds']

    third_tag_response = client.post(
        '/api/admin/blog-tags',
        headers=headers,
        json={'name': 'Admin FastAPI', 'slug': 'admin-fastapi'},
    )
    assert third_tag_response.status_code == 201
    third_tag_id = third_tag_response.json()['id']

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
            'tagIds': [first_tag_id, third_tag_id],
        },
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated['status'] == 'published'
    assert updated['isFeatured'] is True
    assert 'Admin FastAPI' in updated['tagNames']


def test_admin_can_manage_taxonomy_experience_navigation_and_stats(client: TestClient) -> None:
    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    category_response = client.post(
        '/api/admin/skill-categories',
        headers=headers,
        json={'name': 'Backend', 'description': 'Backend skills', 'sortOrder': 25},
    )
    assert category_response.status_code == 201
    category_id = category_response.json()['id']

    skill_response = client.post(
        '/api/admin/skills',
        headers=headers,
        json={
            'categoryId': category_id,
            'name': 'FastAPI Admin Skill',
            'yearsOfExperience': 2,
            'iconKey': 'server',
            'sortOrder': 10,
            'isHighlighted': True,
        },
    )
    assert skill_response.status_code == 201
    skill_id = skill_response.json()['id']

    experience_response = client.post(
        '/api/admin/experiences',
        headers=headers,
        json={
            'organizationName': 'OpenAI',
            'roleTitle': 'Builder',
            'location': 'Remote',
            'experienceType': 'work',
            'startDate': '2026-01-01',
            'endDate': None,
            'isCurrent': True,
            'summary': 'Building portfolio CMS features',
            'descriptionMarkdown': 'Experience body',
            'logoFileId': None,
            'sortOrder': 5,
            'skillIds': [skill_id],
        },
    )
    assert experience_response.status_code == 201
    assert experience_response.json()['skills'][0]['id'] == skill_id

    navigation_response = client.post(
        '/api/admin/navigation-items',
        headers=headers,
        json={
            'label': 'Admin',
            'routePath': '/admin',
            'isExternal': False,
            'sortOrder': 99,
            'isVisible': True,
        },
    )
    assert navigation_response.status_code == 201
    assert navigation_response.json()['routePath'] == '/admin'

    snapshot_response = client.post(
        '/api/admin/github-snapshots',
        headers=headers,
        json={
            'snapshotDate': '2026-04-11',
            'username': 'shuzu',
            'publicRepoCount': 12,
            'followersCount': 10,
            'followingCount': 5,
            'totalStars': 22,
            'totalCommits': 100,
            'rawPayload': {'source': 'test'},
            'contributionDays': [
                {'date': '2026-04-10', 'count': 4, 'level': 2},
                {'date': '2026-04-11', 'count': 1, 'level': 1},
            ],
        },
    )
    assert snapshot_response.status_code == 201
    assert len(snapshot_response.json()['contributionDays']) == 2

    admin_response = client.post(
        '/api/admin/admin-users',
        headers=headers,
        json={
            'email': 'editor@example.com',
            'displayName': 'Editor',
            'password': 'editor-password',
            'isActive': True,
        },
    )
    assert admin_response.status_code == 201
    assert admin_response.json()['email'] == 'editor@example.com'


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


def test_admin_can_refresh_github_snapshot_from_github(client: TestClient, monkeypatch) -> None:
    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    call_count = {'value': 0}

    def fake_sync_profile(self, username: str | None = None) -> SyncedGithubSnapshot:
        call_count['value'] += 1
        return SyncedGithubSnapshot(
            snapshot_date='2026-04-11',
            username=username or 'Alex-v-p',
            public_repo_count=5,
            followers_count=3,
            following_count=1,
            total_stars=9,
            total_commits=14 + call_count['value'],
            raw_payload={'source': 'test-refresh', 'run': call_count['value']},
            contribution_days=[
                SyncedGithubContributionDay(date='2026-04-10', count=4, level=2),
                SyncedGithubContributionDay(date='2026-04-11', count=6 + call_count['value'], level=3),
            ],
        )

    monkeypatch.setattr('app.api.routes.admin.GithubStatsSyncService.sync_profile', fake_sync_profile)

    first_response = client.post('/api/admin/github-snapshots/refresh', headers=headers, json={'username': 'Alex-v-p', 'pruneHistory': True})
    assert first_response.status_code == 200
    first_snapshot = first_response.json()
    assert first_snapshot['username'] == 'Alex-v-p'
    assert first_snapshot['totalCommits'] == 15

    second_response = client.post('/api/admin/github-snapshots/refresh', headers=headers, json={'username': 'Alex-v-p', 'pruneHistory': True})
    assert second_response.status_code == 200
    second_snapshot = second_response.json()
    assert second_snapshot['totalCommits'] == 16

    listing_response = client.get('/api/admin/github-snapshots', headers=headers)
    assert listing_response.status_code == 200
    matching_snapshots = [item for item in listing_response.json()['items'] if item['username'] == 'Alex-v-p']
    assert len(matching_snapshots) == 1
    assert matching_snapshots[0]['id'] == second_snapshot['id']


def test_admin_can_rebuild_assistant_knowledge_index(client: TestClient) -> None:
    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    status_response = client.get('/api/admin/assistant/knowledge', headers=headers)
    assert status_response.status_code == 200
    initial_status = status_response.json()
    assert 'totalDocuments' in initial_status
    assert 'totalChunks' in initial_status

    rebuild_response = client.post('/api/admin/assistant/knowledge/rebuild', headers=headers, json={})
    assert rebuild_response.status_code == 200
    rebuilt = rebuild_response.json()
    assert rebuilt['totalDocuments'] >= 1
    assert rebuilt['totalChunks'] >= rebuilt['totalDocuments']
    assert rebuilt['documentsBySourceType']



def test_admin_refresh_returns_async_task_when_redis_queue_is_available(client: TestClient, monkeypatch) -> None:
    from app.services.async_tasks import AdminTaskRecord

    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    class FakeQueue:
        enabled = True
        poll_after_ms = 1200

        def enqueue(self, task_type: str, payload: dict[str, object]) -> AdminTaskRecord:
            assert task_type == 'github-refresh'
            assert payload['username'] == 'Alex-v-p'
            return AdminTaskRecord(task_id='task-1', task_type=task_type, status='queued', submitted_at='2026-04-14T10:00:00+00:00')

    monkeypatch.setattr('app.api.routes.admin.stats.get_admin_task_queue', lambda: FakeQueue())

    response = client.post('/api/admin/github-snapshots/refresh', headers=headers, json={'username': 'Alex-v-p', 'pruneHistory': True})
    assert response.status_code == 202
    assert response.json() == {
        'taskId': 'task-1',
        'taskType': 'github-refresh',
        'status': 'queued',
        'pollAfterMs': 1200,
    }


def test_admin_can_fetch_async_task_status(client: TestClient, monkeypatch) -> None:
    from app.services.async_tasks import AdminTaskRecord

    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    class FakeQueue:
        def get(self, task_id: str) -> AdminTaskRecord | None:
            assert task_id == 'task-1'
            return AdminTaskRecord(
                task_id='task-1',
                task_type='assistant-knowledge-rebuild',
                status='succeeded',
                submitted_at='2026-04-14T10:00:00+00:00',
                started_at='2026-04-14T10:00:01+00:00',
                completed_at='2026-04-14T10:00:05+00:00',
                result={'totalDocuments': 5, 'totalChunks': 12},
            )

    monkeypatch.setattr('app.api.routes.admin.tasks.get_admin_task_queue', lambda: FakeQueue())

    response = client.get('/api/admin/tasks/task-1', headers=headers)
    assert response.status_code == 200
    assert response.json()['status'] == 'succeeded'
    assert response.json()['result']['totalDocuments'] == 5


def test_admin_site_activity_includes_retention_countdowns(client: TestClient) -> None:
    from datetime import UTC, datetime, timedelta

    from sqlalchemy.orm import Session

    from app.db.models import AssistantConversation, AssistantMessage, AssistantRole, EventType, SiteEvent
    from app.db.session import get_engine

    now = datetime.now(UTC)
    event_created_at = now - timedelta(days=10)
    conversation_last_message_at = now - timedelta(days=4)
    conversation_id = ''

    with Session(get_engine()) as session:
        conversation = AssistantConversation(
            session_id='assistant-session-1',
            started_at=conversation_last_message_at - timedelta(minutes=5),
            last_message_at=conversation_last_message_at,
        )
        session.add(
            SiteEvent(
                visitor_id='visitor-retention',
                session_id='visit-retention',
                page_path='/assistant',
                event_type=EventType.ASSISTANT_MESSAGE,
                metadata_json={'conversation_id': None},
                created_at=event_created_at,
            )
        )
        session.add(conversation)
        session.flush()
        conversation_id = str(conversation.id)
        session.add(
            AssistantMessage(
                conversation_id=conversation.id,
                role=AssistantRole.USER,
                message_text='How long until this disappears?',
                created_at=conversation_last_message_at,
            )
        )
        session.add(
            SiteEvent(
                visitor_id='visitor-retention',
                session_id='visit-retention',
                page_path='/assistant',
                event_type=EventType.ASSISTANT_MESSAGE,
                metadata_json={'conversation_id': conversation_id, 'used_fallback': False},
                created_at=conversation_last_message_at,
            )
        )
        session.commit()

    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/admin/site-activity', headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body['summary']['siteEventsRetentionDays'] == 90
    assert body['summary']['assistantActivityRetentionDays'] == 90

    tracked_event = next(item for item in body['events'] if item['visitorId'] == 'visitor-retention' and item['createdAt'] == event_created_at.isoformat())
    assert tracked_event['retentionEndsAt'] == (event_created_at + timedelta(days=90)).isoformat()
    assert tracked_event['secondsUntilRetentionEnd'] > 0

    tracked_visitor = next(item for item in body['visitors'] if item['visitorId'] == 'visitor-retention')
    assert tracked_visitor['retentionEndsAt'] == (conversation_last_message_at + timedelta(days=90)).isoformat()
    assert tracked_visitor['secondsUntilRetentionEnd'] > 0

    tracked_visit = next(item for item in body['visits'] if item['sessionId'] == 'visit-retention')
    assert tracked_visit['retentionEndsAt'] == (conversation_last_message_at + timedelta(days=90)).isoformat()
    assert tracked_visit['secondsUntilRetentionEnd'] > 0

    tracked_conversation = next(item for item in body['assistantConversations'] if item['id'] == conversation_id)
    assert tracked_conversation['retentionEndsAt'] == (conversation_last_message_at + timedelta(days=90)).isoformat()
    assert tracked_conversation['secondsUntilRetentionEnd'] > 0



def test_admin_github_snapshot_listing_includes_auto_refresh_countdown(client: TestClient, monkeypatch) -> None:
    from datetime import datetime, timezone

    from app.services.maintenance import MaintenanceJobStatus

    token = _admin_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    created_response = client.post(
        '/api/admin/github-snapshots',
        headers=headers,
        json={
            'snapshotDate': '2026-04-11',
            'username': 'Alex-v-p',
            'publicRepoCount': 12,
            'followersCount': 10,
            'followingCount': 5,
            'totalStars': 22,
            'totalCommits': 100,
            'rawPayload': {'source': 'test'},
            'contributionDays': [],
        },
    )
    assert created_response.status_code == 201

    next_run_at = datetime(2026, 4, 15, 9, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(
        'app.domains.admin.repository.stats.MaintenanceJobInspector.github_auto_refresh_status',
        lambda self, now=None: MaintenanceJobStatus(
            enabled=True,
            status='scheduled',
            next_run_at=next_run_at,
            seconds_until_next_run=3600,
            last_attempt_at=datetime(2026, 4, 14, 8, 0, tzinfo=timezone.utc),
            last_success_at=datetime(2026, 4, 14, 8, 0, tzinfo=timezone.utc),
            last_failed_at=None,
            last_error=None,
        ),
    )

    response = client.get('/api/admin/github-snapshots', headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body['autoRefreshEnabled'] is True
    assert body['autoRefreshStatus'] == 'scheduled'
    assert body['nextAutoRefreshAt'] == next_run_at.isoformat()
    assert body['secondsUntilAutoRefresh'] == 3600

    snapshot = next(item for item in body['items'] if item['username'] == 'Alex-v-p')
    assert snapshot['autoRefreshEnabled'] is True
    assert snapshot['autoRefreshStatus'] == 'scheduled'
    assert snapshot['nextAutoRefreshAt'] == next_run_at.isoformat()
    assert snapshot['secondsUntilAutoRefresh'] == 3600
