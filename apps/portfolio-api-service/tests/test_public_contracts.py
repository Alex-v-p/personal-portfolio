from __future__ import annotations

from fastapi.testclient import TestClient


EXPECTED_SITE_SHELL_KEYS = {'navigation', 'profile', 'footerText', 'contactMethods'}
EXPECTED_NAVIGATION_ITEM_KEYS = {'id', 'label', 'routePath', 'isExternal', 'sortOrder', 'isVisible'}
EXPECTED_PROFILE_KEYS = {
    'id', 'firstName', 'lastName', 'headline', 'shortIntro', 'longBio', 'location', 'email', 'phone',
    'avatarFileId', 'heroImageFileId', 'resumeFileId', 'avatar', 'heroImage', 'resume', 'ctaPrimaryLabel',
    'ctaPrimaryUrl', 'ctaSecondaryLabel', 'ctaSecondaryUrl', 'isPublic', 'socialLinks', 'footerDescription',
    'introParagraphs', 'availability', 'skills', 'expertiseGroups', 'createdAt', 'updatedAt'
}
EXPECTED_PROJECT_SUMMARY_KEYS = {
    'id', 'slug', 'title', 'teaser', 'summary', 'coverImageFileId', 'coverImage',
    'githubUrl', 'githubRepoOwner', 'githubRepoName', 'demoUrl', 'companyName', 'startedOn', 'endedOn',
    'durationLabel', 'status', 'state', 'isFeatured', 'sortOrder', 'publishedAt', 'createdAt', 'updatedAt',
    'skills'
}
EXPECTED_PROJECT_DETAIL_KEYS = EXPECTED_PROJECT_SUMMARY_KEYS | {'descriptionMarkdown', 'images'}
EXPECTED_BLOG_POST_SUMMARY_KEYS = {
    'id', 'slug', 'title', 'excerpt', 'coverImageFileId', 'coverImageAlt', 'coverImage',
    'readingTimeMinutes', 'status', 'isFeatured', 'publishedAt', 'createdAt', 'updatedAt', 'tags'
}
EXPECTED_BLOG_POST_DETAIL_KEYS = EXPECTED_BLOG_POST_SUMMARY_KEYS | {'contentMarkdown', 'seoTitle', 'seoDescription'}


def test_site_shell_contract_matches_frontend_expectations(client: TestClient) -> None:
    response = client.get('/api/public/site-shell')
    assert response.status_code == 200
    body = response.json()

    assert EXPECTED_SITE_SHELL_KEYS <= set(body)
    assert {'items', 'total'} <= set(body['navigation'])
    assert body['navigation']['items']
    assert EXPECTED_NAVIGATION_ITEM_KEYS <= set(body['navigation']['items'][0])
    assert EXPECTED_PROFILE_KEYS <= set(body['profile'])
    assert {'platform', 'label', 'value', 'href', 'actionLabel', 'sortOrder', 'isVisible'} <= set(body['contactMethods'][0])


def test_home_contract_matches_frontend_expectations(client: TestClient) -> None:
    response = client.get('/api/public/home')
    assert response.status_code == 200
    body = response.json()

    assert {'hero', 'featuredProjects', 'featuredBlogPosts', 'expertiseGroups', 'experiencePreview', 'contactPreview'} <= set(body)
    assert EXPECTED_PROFILE_KEYS <= set(body['hero'])
    assert body['featuredProjects']
    assert EXPECTED_PROJECT_SUMMARY_KEYS <= set(body['featuredProjects'][0])
    assert 'descriptionMarkdown' not in body['featuredProjects'][0]
    assert body['featuredBlogPosts']
    assert EXPECTED_BLOG_POST_SUMMARY_KEYS <= set(body['featuredBlogPosts'][0])
    assert 'contentMarkdown' not in body['featuredBlogPosts'][0]


def test_project_detail_contract_matches_frontend_expectations(client: TestClient) -> None:
    response = client.get('/api/public/projects/personal-portfolio')
    assert response.status_code == 200
    body = response.json()

    assert EXPECTED_PROJECT_DETAIL_KEYS <= set(body)
    assert {'id', 'url', 'alt', 'fileName', 'mimeType', 'width', 'height'} <= set(body['coverImage'])
    assert {'id', 'name', 'sortOrder', 'isHighlighted'} <= set(body['skills'][0])


def test_blog_post_detail_contract_matches_frontend_expectations(client: TestClient) -> None:
    response = client.get('/api/public/blog-posts/building-a-portfolio-shell')
    assert response.status_code == 200
    body = response.json()

    assert EXPECTED_BLOG_POST_DETAIL_KEYS <= set(body)
    assert {'id', 'url', 'alt', 'fileName', 'mimeType', 'width', 'height'} <= set(body['coverImage'])
    assert {'id', 'name', 'slug'} <= set(body['tags'][0])
