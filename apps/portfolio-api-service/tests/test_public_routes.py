from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_profile_returns_seeded_profile() -> None:
    response = client.get('/api/public/profile')

    assert response.status_code == 200
    body = response.json()
    assert body['id'] == 'profile-alex-van-poppel'
    assert body['heroActions'][0]['label'] == 'Download CV'


def test_list_projects_returns_seeded_projects() -> None:
    response = client.get('/api/public/projects')

    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 5
    assert body['items'][0]['slug'] == 'personal-portfolio'
    assert 'tags' in body['items'][0]



def test_list_blog_posts_returns_seeded_articles() -> None:
    response = client.get('/api/public/blog-posts')

    assert response.status_code == 200
    body = response.json()
    assert body['total'] >= 4
    slugs = {item['slug'] for item in body['items']}
    assert 'building-a-portfolio-shell' in slugs
    assert 'contentMarkdown' in body['items'][0]

def test_get_blog_post_by_slug_returns_single_article() -> None:
    response = client.get('/api/public/blog-posts/building-a-portfolio-shell')

    assert response.status_code == 200
    body = response.json()
    assert body['slug'] == 'building-a-portfolio-shell'
    assert body['status'] == 'published'
