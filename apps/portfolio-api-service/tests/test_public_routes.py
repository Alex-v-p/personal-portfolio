from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient


def test_get_profile_returns_media_and_derived_fields(client: TestClient) -> None:
    response = client.get('/api/public/profile')
    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['headline'] == 'Software Engineer'
    assert body['avatar']['url'].startswith('http://media.example.test/portfolio/profiles/alex/')
    assert body['ctaPrimaryUrl'].startswith('http://media.example.test/portfolio/profiles/alex/resume.pdf')
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
    assert body['featuredBlogPosts']
    assert body['experiencePreview']
    assert body['contactPreview']


def test_list_projects_returns_embedded_media(client: TestClient) -> None:
    response = client.get('/api/public/projects')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 5
    project = body['items'][0]
    UUID(project['id'])
    assert project['coverImage']['url'].startswith('http://media.example.test/portfolio/projects/')
    assert project['skills'][0]['name']
    assert 'tags' not in project


def test_get_project_by_slug_returns_project_detail(client: TestClient) -> None:
    response = client.get('/api/public/projects/personal-portfolio')
    assert response.status_code == 200
    body = response.json()
    assert body['slug'] == 'personal-portfolio'
    assert body['images']
    assert body['coverImage']['url'].startswith('http://media.example.test/portfolio/projects/')


def test_list_blog_posts_returns_embedded_cover_media(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 4
    assert body['items'][0]['coverImage']['url'].startswith('http://media.example.test/portfolio/blog/')
    assert body['items'][0]['tags']


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
