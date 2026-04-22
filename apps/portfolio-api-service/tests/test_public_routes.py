from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi.testclient import TestClient

from app.db.models import BlogPost, EventType, MediaFile, MediaVisibility, Project, ProjectState, PublicationStatus, SiteEvent
from app.db.session import get_session_factory
from infra.postgres.bootstrap.seed_content import BLOG_POST_ROWS, PROFILE_ROW, PROJECT_ROWS
from infra.postgres.bootstrap.seed_data import GITHUB_SNAPSHOT, SITE_EVENT_ROWS
from infra.postgres.bootstrap.seed_ids import seed_uuid


def _find_project_slug(*, title_contains: str | None = None) -> str:
    for project in PROJECT_ROWS:
        if title_contains is None or title_contains.lower() in project['title'].lower():
            return project['slug']
    return PROJECT_ROWS[0]['slug']


def _find_project_id(*, title_contains: str | None = None) -> str:
    for project in PROJECT_ROWS:
        if title_contains is None or title_contains.lower() in project['title'].lower():
            return project['id']
    return PROJECT_ROWS[0]['id']


def _find_blog_slug(*, title_contains: str | None = None) -> str:
    for post in BLOG_POST_ROWS:
        if title_contains is None or title_contains.lower() in post['title'].lower():
            return post['slug']
    return BLOG_POST_ROWS[0]['slug']


def test_get_profile_returns_media_and_derived_fields(client: TestClient) -> None:
    response = client.get('/api/public/profile')
    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['headline'] == PROFILE_ROW['headline']
    assert body['avatar']['url'].startswith('http://media.example.test/portfolio/profiles/')
    assert body['resume']['mimeType'] == 'application/pdf'
    assert body['skills']
    assert body['expertiseGroups']
    assert body['expertiseGroups'][0]['iconKey']
    assert 'iconKey' in body['expertiseGroups'][0]['skills'][0]
    assert body['socialLinks'][0]['platform'] == 'github'
    assert 'iconKey' in body['socialLinks'][0]


def test_get_navigation_returns_visible_items(client: TestClient) -> None:
    response = client.get('/api/public/navigation')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 5
    assert body['items'][0]['routePath'].startswith('/')


def test_get_site_shell_returns_navigation_profile_and_contact_methods(client: TestClient) -> None:
    response = client.get('/api/public/site-shell')
    assert response.status_code == 200
    body = response.json()
    assert body['navigation']['items']
    assert body['profile']['firstName'] == PROFILE_ROW['first_name']
    assert body['contactMethods']
    assert body['contactMethods'][0]['iconKey']
    assert body['footerText']


def test_get_home_returns_composed_public_sections(client: TestClient) -> None:
    response = client.get('/api/public/home')
    assert response.status_code == 200
    body = response.json()
    assert body['hero']['headline'] == PROFILE_ROW['headline']
    assert body['featuredProjects']
    assert 'descriptionMarkdown' not in body['featuredProjects'][0]
    assert body['featuredBlogPosts']
    assert 'contentMarkdown' not in body['featuredBlogPosts'][0]
    assert body['experiencePreview']
    assert body['expertiseGroups'][0]['iconKey']
    assert 'iconKey' in body['expertiseGroups'][0]['skills'][0]
    assert body['contactPreview']
    assert body['contactPreview'][0]['iconKey']


def test_list_projects_returns_project_summaries_with_embedded_media(client: TestClient) -> None:
    response = client.get('/api/public/projects')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] == len(PROJECT_ROWS)
    project = body['items'][0]
    UUID(project['id'])
    assert project['coverImage']['url'].startswith('http://media.example.test/portfolio/projects/')
    assert project['skills'][0]['name']
    assert 'descriptionMarkdown' not in project
    assert 'images' not in project
    assert 'tags' not in project


def test_get_project_by_slug_returns_project_detail(client: TestClient) -> None:
    slug = _find_project_slug(title_contains='portfolio')
    response = client.get(f'/api/public/projects/{slug}')
    assert response.status_code == 200
    body = response.json()
    assert body['slug'] == slug
    assert body['images']
    assert body['coverImage']['url'].startswith('http://media.example.test/portfolio/projects/')


def test_list_blog_posts_returns_blog_post_summaries_with_embedded_cover_media(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] == len(BLOG_POST_ROWS)
    assert body['items'][0]['coverImage']['url'].startswith('http://media.example.test/portfolio/blog/')
    assert body['items'][0]['tags']
    assert 'contentMarkdown' not in body['items'][0]
    assert 'seoTitle' not in body['items'][0]


def test_get_blog_post_by_slug_returns_single_article(client: TestClient) -> None:
    slug = _find_blog_slug(title_contains='homelab')
    response = client.get(f'/api/public/blog-posts/{slug}')
    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['slug'] == slug
    assert body['status'] == 'published'
    assert body['coverImage']['url'].startswith('http://media.example.test/portfolio/blog/')


def test_list_experience_returns_rows_with_skill_names(client: TestClient) -> None:
    response = client.get('/api/public/experience')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 3
    assert body['items'][0]['skillNames']


def test_get_github_snapshot_returns_latest_snapshot(client: TestClient) -> None:
    response = client.get('/api/public/github')
    assert response.status_code == 200
    body = response.json()
    assert body['username'] == GITHUB_SNAPSHOT['username']
    assert body['contributionDays']


def test_get_stats_returns_api_backed_stats_payload(client: TestClient) -> None:
    baseline_views = sum(1 for event in SITE_EVENT_ROWS if event['event_type'] == EventType.PAGE_VIEW)
    baseline_likes = sum(1 for event in SITE_EVENT_ROWS if event['event_type'] == EventType.PORTFOLIO_LIKE)

    session_factory = get_session_factory()
    with session_factory() as session:
        session.add_all(
            [
                SiteEvent(visitor_id='visitor-a', session_id='session-a', page_path='/', event_type=EventType.PAGE_VIEW),
                SiteEvent(visitor_id='visitor-b', session_id='session-b', page_path='/projects', event_type=EventType.PAGE_VIEW),
                SiteEvent(visitor_id='visitor-a', session_id='session-a', page_path='/stats', event_type=EventType.PORTFOLIO_LIKE),
            ]
        )
        session.commit()

    response = client.get('/api/public/stats')
    assert response.status_code == 200
    body = response.json()
    assert body['githubSummary']['label'] == 'Public repos'
    assert body['latestGithubSnapshot']['username'] == GITHUB_SNAPSHOT['username']
    assert body['portfolioHighlights'][0]['label'] == 'Total views'
    assert body['portfolioHighlights'][0]['value'] == str(baseline_views + 2)
    assert body['portfolioHighlights'][1]['label'] == 'Like counter'
    assert body['portfolioHighlights'][1]['value'] == str(baseline_likes + 1)
    assert len(body['contributionWeeks']) >= 52
    assert len(body['monthLabels']) == len(body['contributionWeeks'])




def test_public_routes_return_localized_dutch_content_when_available(client: TestClient) -> None:
    profile_response = client.get('/api/public/profile', params={'locale': 'nl'})
    assert profile_response.status_code == 200
    profile_body = profile_response.json()
    assert profile_body['headline'] == PROFILE_ROW['headline_nl']
    assert profile_body['ctaPrimaryLabel'] == PROFILE_ROW['cta_primary_label_nl']

    navigation_response = client.get('/api/public/navigation', params={'locale': 'nl'})
    assert navigation_response.status_code == 200
    navigation_body = navigation_response.json()
    assert navigation_body['items'][1]['label'] == 'Projecten'

    project_response = client.get('/api/public/projects', params={'locale': 'nl'})
    assert project_response.status_code == 200
    assert project_response.json()['items'][0]['durationLabel'].endswith('maanden') or project_response.json()['items'][0]['durationLabel'].endswith('maand')

    blog_slug = _find_blog_slug(title_contains='homelab')
    blog_response = client.get(f'/api/public/blog-posts/{blog_slug}', params={'locale': 'nl'})
    assert blog_response.status_code == 200
    assert blog_response.json()['title'] == 'Mijn homelab'


def test_public_routes_fall_back_to_english_when_locale_content_is_missing(client: TestClient) -> None:
    session_factory = get_session_factory()
    with session_factory() as session:
        project = session.get(Project, seed_uuid(_find_project_id(title_contains='portfolio')))
        assert project is not None
        project.title_nl = None
        project.summary_nl = None
        project.description_markdown_nl = None
        session.commit()

    response = client.get(f"/api/public/projects/{_find_project_slug(title_contains='portfolio')}", params={'locale': 'nl'})
    assert response.status_code == 200
    body = response.json()
    assert body['title'] == 'Old Laravel Portfolio'
    assert body['descriptionMarkdown'].startswith('## Why I built it')

def test_public_projects_exclude_archived_or_scheduled_records(client: TestClient) -> None:
    session_factory = get_session_factory()
    with session_factory() as session:
        archived_project = Project(
            id=seed_uuid('project-archived-hidden'),
            slug='archived-hidden-project',
            title='Archived hidden project',
            teaser='Should not be public.',
            summary='Should stay hidden.',
            description_markdown='Hidden archived project.',
            duration_label='1 week',
            status='Archived',
            state=ProjectState.ARCHIVED,
            is_featured=True,
            sort_order=999,
            published_at=datetime.now(UTC) - timedelta(days=3),
        )
        scheduled_project = Project(
            id=seed_uuid('project-scheduled-hidden'),
            slug='scheduled-hidden-project',
            title='Scheduled hidden project',
            teaser='Should not be public yet.',
            summary='Future project.',
            description_markdown='Scheduled project.',
            duration_label='2 weeks',
            status='Scheduled',
            state=ProjectState.PUBLISHED,
            is_featured=True,
            sort_order=998,
            published_at=datetime.now(UTC) + timedelta(days=7),
        )
        session.add_all([archived_project, scheduled_project])
        session.commit()

    listing = client.get('/api/public/projects')
    assert listing.status_code == 200
    slugs = {item['slug'] for item in listing.json()['items']}
    assert 'archived-hidden-project' not in slugs
    assert 'scheduled-hidden-project' not in slugs

    assert client.get('/api/public/projects/archived-hidden-project').status_code == 404
    assert client.get('/api/public/projects/scheduled-hidden-project').status_code == 404


def test_public_blog_posts_exclude_drafts_and_future_posts(client: TestClient) -> None:
    session_factory = get_session_factory()
    with session_factory() as session:
        draft_post = BlogPost(
            id=seed_uuid('post-draft-hidden'),
            slug='draft-hidden-post',
            title='Draft hidden post',
            excerpt='Should not be public.',
            content_markdown='Draft content.',
            status=PublicationStatus.DRAFT,
            is_featured=True,
            published_at=None,
        )
        future_post = BlogPost(
            id=seed_uuid('post-future-hidden'),
            slug='future-hidden-post',
            title='Future hidden post',
            excerpt='Should not be public yet.',
            content_markdown='Future content.',
            status=PublicationStatus.PUBLISHED,
            is_featured=True,
            published_at=datetime.now(UTC) + timedelta(days=2),
        )
        session.add_all([draft_post, future_post])
        session.commit()

    listing = client.get('/api/public/blog-posts')
    assert listing.status_code == 200
    slugs = {item['slug'] for item in listing.json()['items']}
    assert 'draft-hidden-post' not in slugs
    assert 'future-hidden-post' not in slugs

    assert client.get('/api/public/blog-posts/draft-hidden-post').status_code == 404
    assert client.get('/api/public/blog-posts/future-hidden-post').status_code == 404


def test_public_media_mapping_hides_non_public_assets(client: TestClient) -> None:
    session_factory = get_session_factory()
    with session_factory() as session:
        private_file = MediaFile(
            id=seed_uuid('file-private-cover-image'),
            bucket_name='portfolio',
            object_key='private/cover.png',
            original_filename='private-cover.png',
            stored_filename='private-cover.png',
            mime_type='image/png',
            visibility=MediaVisibility.PRIVATE,
        )
        project = session.get(Project, seed_uuid(_find_project_id(title_contains='portfolio')))
        assert project is not None
        session.add(private_file)
        session.flush()
        project.cover_image_file_id = private_file.id
        session.commit()

    response = client.get(f"/api/public/projects/{_find_project_slug(title_contains='portfolio')}")
    assert response.status_code == 200
    body = response.json()
    assert body['coverImage'] is None
