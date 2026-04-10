from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient


def test_get_profile_returns_seeded_profile(client: TestClient) -> None:
    response = client.get('/api/public/profile')

    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['heroActions'][0]['label'] == 'Download CV'


def test_list_projects_returns_seeded_projects(client: TestClient) -> None:
    response = client.get('/api/public/projects')

    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 5
    UUID(body['items'][0]['id'])
    assert body['items'][0]['slug'] == 'personal-portfolio'
    assert 'tags' in body['items'][0]


def test_list_blog_posts_returns_seeded_articles(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts')

    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 4
    UUID(body['items'][0]['id'])
    slugs = {item['slug'] for item in body['items']}
    assert 'building-a-portfolio-shell' in slugs
    assert 'contentMarkdown' in body['items'][0]


def test_get_blog_post_by_slug_returns_single_article(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts/building-a-portfolio-shell')

    assert response.status_code == 200
    body = response.json()
    UUID(body['id'])
    assert body['slug'] == 'building-a-portfolio-shell'
    assert body['status'] == 'published'
