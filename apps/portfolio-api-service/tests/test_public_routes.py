from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient


def test_get_profile_returns_schema_shaped_profile(client: TestClient) -> None:
    response = client.get('/api/public/profile')

    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['headline'] == 'Software Engineer'
    assert body['socialLinks'][0]['platform'] == 'github'
    assert 'heroActions' not in body


def test_list_projects_returns_schema_shaped_projects(client: TestClient) -> None:
    response = client.get('/api/public/projects')

    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 5
    first_project = body['items'][0]
    UUID(first_project['id'])
    assert first_project['slug'] == 'personal-portfolio'
    assert 'skills' in first_project
    assert 'images' in first_project
    assert 'tags' not in first_project
    assert first_project['skills'][0]['name'] == 'Angular'


def test_list_blog_posts_returns_schema_shaped_articles(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts')

    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 4
    UUID(body['items'][0]['id'])
    slugs = {item['slug'] for item in body['items']}
    assert 'building-a-portfolio-shell' in slugs
    assert 'contentMarkdown' in body['items'][0]
    assert isinstance(body['items'][0]['tags'][0], dict)


def test_get_blog_post_by_slug_returns_single_article(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts/building-a-portfolio-shell')

    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['slug'] == 'building-a-portfolio-shell'
    assert body['status'] == 'published'
    assert body['tags'][0]['slug']
