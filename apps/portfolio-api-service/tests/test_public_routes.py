from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi.testclient import TestClient

from app.db.models import BlogPost, MediaFile, MediaVisibility, Project, ProjectState, PublicationStatus
from app.db.session import get_session_factory
from infra.postgres.bootstrap.seed_ids import seed_uuid


def test_get_profile_returns_media_and_derived_fields(client: TestClient) -> None:
    response = client.get('/api/public/profile')
    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['headline'] == 'Software Engineer'
    assert body['avatar']['url'].startswith('http://media.example.test/portfolio/profiles/')
    assert body['resume']['mimeType'] == 'application/pdf'
    assert body['skills']
    assert body['expertiseGroups']
    assert body['socialLinks'][0]['platform'] == 'github'


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
    assert body['profile']['firstName'] == 'Alex'
    assert body['contactMethods']
    assert body['footerText']


def test_get_home_returns_composed_public_sections(client: TestClient) -> None:
    response = client.get('/api/public/home')
    assert response.status_code == 200
    body = response.json()
    assert body['hero']['headline'] == 'Software Engineer'
    assert body['featuredProjects']
    assert 'descriptionMarkdown' not in body['featuredProjects'][0]
    assert body['featuredBlogPosts']
    assert 'contentMarkdown' not in body['featuredBlogPosts'][0]
    assert body['experiencePreview']
    assert body['contactPreview']


def test_list_projects_returns_project_summaries_with_embedded_media(client: TestClient) -> None:
    response = client.get('/api/public/projects')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 5
    project = body['items'][0]
    UUID(project['id'])
    assert project['coverImage']['url'].startswith('http://media.example.test/portfolio/projects/')
    assert project['skills'][0]['name']
    assert 'descriptionMarkdown' not in project
    assert 'images' not in project
    assert 'tags' not in project


def test_get_project_by_slug_returns_project_detail(client: TestClient) -> None:
    response = client.get('/api/public/projects/personal-portfolio')
    assert response.status_code == 200
    body = response.json()
    assert body['slug'] == 'personal-portfolio'
    assert body['images']
    assert body['coverImage']['url'].startswith('http://media.example.test/portfolio/projects/')


def test_list_blog_posts_returns_blog_post_summaries_with_embedded_cover_media(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 4
    assert body['items'][0]['coverImage']['url'].startswith('http://media.example.test/portfolio/blog/')
    assert body['items'][0]['tags']
    assert 'contentMarkdown' not in body['items'][0]
    assert 'seoTitle' not in body['items'][0]


def test_get_blog_post_by_slug_returns_single_article(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts/building-a-portfolio-shell')
    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['slug'] == 'building-a-portfolio-shell'
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
    assert body['username'] == 'shuzu'
    assert body['contributionDays']


def test_get_stats_returns_api_backed_stats_payload(client: TestClient) -> None:
    response = client.get('/api/public/stats')
    assert response.status_code == 200
    body = response.json()
    assert body['githubSummary']['label'] == 'GitHub activity'
    assert body['latestGithubSnapshot']['username'] == 'shuzu'
    assert body['portfolioStats']
    assert body['contributionWeeks']


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
        project = session.get(Project, seed_uuid('project-personal-portfolio'))
        assert project is not None
        session.add(private_file)
        session.flush()
        project.cover_image_file_id = private_file.id
        session.commit()

    response = client.get('/api/public/projects/personal-portfolio')
    assert response.status_code == 200
    body = response.json()
    assert body['coverImage'] is None
