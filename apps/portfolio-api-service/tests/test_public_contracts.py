from __future__ import annotations

from fastapi.testclient import TestClient

from infra.postgres.bootstrap.seed_content import BLOG_POST_ROWS, PROJECT_ROWS


EXPECTED_SITE_SHELL_KEYS = {'navigation', 'profile', 'footerText', 'contactMethods'}
EXPECTED_NAVIGATION_ITEM_KEYS = {'id', 'label', 'routePath', 'isExternal', 'sortOrder', 'isVisible'}
EXPECTED_PROFILE_KEYS = {
    'id', 'firstName', 'lastName', 'headline', 'shortIntro', 'longBio', 'location', 'email', 'phone',
    'avatarFileId', 'heroImageFileId', 'resumeFileId', 'avatar', 'heroImage', 'resume', 'ctaPrimaryLabel',
    'ctaPrimaryUrl', 'ctaSecondaryLabel', 'ctaSecondaryUrl', 'isPublic', 'socialLinks', 'footerDescription',
    'introParagraphs', 'availability', 'skills', 'expertiseGroups', 'createdAt', 'updatedAt'
}
EXPECTED_SOCIAL_LINK_KEYS = {'id', 'profileId', 'platform', 'label', 'url', 'iconKey', 'sortOrder', 'isVisible'}
EXPECTED_EXPERTISE_GROUP_KEYS = {'title', 'iconKey', 'tags', 'skills'}
EXPECTED_EXPERTISE_SKILL_KEYS = {'name', 'yearsOfExperience', 'iconKey'}
EXPECTED_CONTACT_METHOD_KEYS = {'id', 'platform', 'label', 'value', 'href', 'actionLabel', 'iconKey', 'sortOrder', 'isVisible'}
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


def _project_slug() -> str:
    for project in PROJECT_ROWS:
        if 'portfolio' in project['title'].lower():
            return project['slug']
    return PROJECT_ROWS[0]['slug']


def _blog_slug() -> str:
    for post in BLOG_POST_ROWS:
        if 'homelab' in post['title'].lower():
            return post['slug']
    return BLOG_POST_ROWS[0]['slug']


def test_site_shell_contract_matches_frontend_expectations(client: TestClient) -> None:
    response = client.get('/api/public/site-shell')
    assert response.status_code == 200
    body = response.json()

    assert EXPECTED_SITE_SHELL_KEYS <= set(body)
    assert {'items', 'total'} <= set(body['navigation'])
    assert body['navigation']['items']
    assert EXPECTED_NAVIGATION_ITEM_KEYS <= set(body['navigation']['items'][0])
    assert EXPECTED_PROFILE_KEYS <= set(body['profile'])
    assert EXPECTED_SOCIAL_LINK_KEYS <= set(body['profile']['socialLinks'][0])
    assert EXPECTED_EXPERTISE_GROUP_KEYS <= set(body['profile']['expertiseGroups'][0])
    assert EXPECTED_EXPERTISE_SKILL_KEYS <= set(body['profile']['expertiseGroups'][0]['skills'][0])
    assert EXPECTED_CONTACT_METHOD_KEYS <= set(body['contactMethods'][0])


def test_home_contract_matches_frontend_expectations(client: TestClient) -> None:
    response = client.get('/api/public/home')
    assert response.status_code == 200
    body = response.json()

    assert {'hero', 'featuredProjects', 'featuredBlogPosts', 'expertiseGroups', 'experiencePreview', 'contactPreview'} <= set(body)
    assert EXPECTED_PROFILE_KEYS <= set(body['hero'])
    assert EXPECTED_EXPERTISE_GROUP_KEYS <= set(body['expertiseGroups'][0])
    assert EXPECTED_EXPERTISE_SKILL_KEYS <= set(body['expertiseGroups'][0]['skills'][0])
    assert EXPECTED_CONTACT_METHOD_KEYS <= set(body['contactPreview'][0])
    assert body['featuredProjects']
    assert EXPECTED_PROJECT_SUMMARY_KEYS <= set(body['featuredProjects'][0])
    assert 'descriptionMarkdown' not in body['featuredProjects'][0]
    assert body['featuredBlogPosts']
    assert EXPECTED_BLOG_POST_SUMMARY_KEYS <= set(body['featuredBlogPosts'][0])
    assert 'contentMarkdown' not in body['featuredBlogPosts'][0]


def test_project_detail_contract_matches_frontend_expectations(client: TestClient) -> None:
    response = client.get(f'/api/public/projects/{_project_slug()}')
    assert response.status_code == 200
    body = response.json()

    assert EXPECTED_PROJECT_DETAIL_KEYS <= set(body)
    assert {'id', 'url', 'alt', 'fileName', 'mimeType', 'width', 'height'} <= set(body['coverImage'])
    assert {'id', 'name', 'iconKey', 'sortOrder', 'isHighlighted'} <= set(body['skills'][0])


def test_blog_post_detail_contract_matches_frontend_expectations(client: TestClient) -> None:
    response = client.get(f'/api/public/blog-posts/{_blog_slug()}')
    assert response.status_code == 200
    body = response.json()

    assert EXPECTED_BLOG_POST_DETAIL_KEYS <= set(body)
    assert {'id', 'url', 'alt', 'fileName', 'mimeType', 'width', 'height'} <= set(body['coverImage'])
    assert {'id', 'name', 'slug'} <= set(body['tags'][0])
