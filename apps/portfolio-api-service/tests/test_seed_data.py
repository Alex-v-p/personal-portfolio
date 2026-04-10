from __future__ import annotations

from app.data.public_content import BLOG_POSTS, PROFILE, PROJECTS
from app.db.seed_data import MEDIA_FILES


def test_all_profile_media_references_exist() -> None:
    media_ids = {item['id'] for item in MEDIA_FILES}

    assert PROFILE['avatar_file_id'] in media_ids
    assert PROFILE['hero_image_file_id'] in media_ids
    assert PROFILE['resume_file_id'] in media_ids


def test_all_project_cover_media_references_exist() -> None:
    media_ids = {item['id'] for item in MEDIA_FILES}

    missing_ids = {project['cover_image_file_id'] for project in PROJECTS if project['cover_image_file_id'] not in media_ids}

    assert missing_ids == set()


def test_all_blog_cover_media_references_exist() -> None:
    media_ids = {item['id'] for item in MEDIA_FILES}

    missing_ids = {post['cover_image_file_id'] for post in BLOG_POSTS if post.get('cover_image_file_id') not in media_ids}

    assert missing_ids == set()
