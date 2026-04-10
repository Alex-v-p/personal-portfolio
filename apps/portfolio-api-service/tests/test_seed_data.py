from __future__ import annotations

import os
from pathlib import Path
from uuid import UUID

from sqlalchemy import create_engine, func, select, text

from app.core.config import get_settings
from app.data.seed_content import BLOG_POST_ROWS, PROFILE_ROW, PROJECT_ROWS
from app.data.seed_ids import seed_uuid
from app.db.init_db import initialize_database
from app.db.models import BlogPost, BlogTag, MediaFile, Profile, Project, ProjectSkill, SocialLink
from app.db.seed_data import MEDIA_FILES
from app.db.session import get_session_factory, reset_database_caches


def test_all_profile_media_references_exist() -> None:
    media_ids = {item['id'] for item in MEDIA_FILES}

    assert PROFILE_ROW['avatar_file_id'] in media_ids
    assert PROFILE_ROW['hero_image_file_id'] in media_ids
    assert PROFILE_ROW['resume_file_id'] in media_ids


def test_all_project_cover_media_references_exist() -> None:
    media_ids = {item['id'] for item in MEDIA_FILES}

    missing_ids = {project['cover_image_file_id'] for project in PROJECT_ROWS if project['cover_image_file_id'] not in media_ids}

    assert missing_ids == set()


def test_all_blog_cover_media_references_exist() -> None:
    media_ids = {item['id'] for item in MEDIA_FILES}

    missing_ids = {post['cover_image_file_id'] for post in BLOG_POST_ROWS if post.get('cover_image_file_id') not in media_ids}

    assert missing_ids == set()


def test_seed_uuid_helper_returns_valid_uuids() -> None:
    assert isinstance(seed_uuid('profile-alex-van-poppel'), UUID)
    assert isinstance(seed_uuid('file-avatar-alex'), UUID)
    assert isinstance(seed_uuid('post-building-a-portfolio-shell'), UUID)


def test_initialize_database_creates_and_seeds_expected_content() -> None:
    reset_database_caches()
    assert initialize_database(auto_seed=True, raise_on_error=True) is True

    session_factory = get_session_factory()
    with session_factory() as session:
        assert session.scalar(select(func.count()).select_from(MediaFile)) == len(MEDIA_FILES)
        assert session.scalar(select(func.count()).select_from(Profile)) == 1
        assert session.scalar(select(func.count()).select_from(Project)) == len(PROJECT_ROWS)
        assert session.scalar(select(func.count()).select_from(BlogPost)) == len(BLOG_POST_ROWS)
        assert session.scalar(select(func.count()).select_from(SocialLink)) >= 3
        assert session.scalar(select(func.count()).select_from(ProjectSkill)) > 0
        assert session.scalar(select(func.count()).select_from(BlogTag)) > 0

        profile = session.scalar(select(Profile))
        project = session.scalar(select(Project).limit(1))
        post = session.scalar(select(BlogPost).limit(1))

        assert isinstance(profile.id, UUID)
        assert isinstance(project.id, UUID)
        assert isinstance(post.id, UUID)

        assert initialize_database(auto_seed=True, raise_on_error=True) is True
        assert session.scalar(select(func.count()).select_from(Project)) == len(PROJECT_ROWS)


def test_initialize_database_recreates_legacy_schema_with_string_foreign_keys(tmp_path: Path) -> None:
    database_path = tmp_path / 'legacy.sqlite3'
    engine = create_engine(f'sqlite:///{database_path}', future=True)
    with engine.begin() as connection:
        connection.execute(text('CREATE TABLE profiles (id CHAR(32) PRIMARY KEY, first_name VARCHAR(120) NOT NULL, last_name VARCHAR(120) NOT NULL, headline VARCHAR(255) NOT NULL, short_intro TEXT NOT NULL, long_bio TEXT, location VARCHAR(255), email VARCHAR(320), phone VARCHAR(64), avatar_file_id CHAR(32), hero_image_file_id CHAR(32), resume_file_id CHAR(32), cta_primary_label VARCHAR(120), cta_primary_url VARCHAR(500), cta_secondary_label VARCHAR(120), cta_secondary_url VARCHAR(500), is_public BOOLEAN NOT NULL, created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL)'))
        connection.execute(text('CREATE TABLE social_links (id CHAR(32) PRIMARY KEY, profile_id VARCHAR(255) NOT NULL, platform VARCHAR(50) NOT NULL, label VARCHAR(120) NOT NULL, url VARCHAR(500) NOT NULL, icon_key VARCHAR(80), sort_order INTEGER NOT NULL, is_visible BOOLEAN NOT NULL)'))

    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['DB_AUTO_CREATE'] = 'true'
    os.environ['DB_AUTO_SEED'] = 'true'
    os.environ['DB_STARTUP_GRACEFUL'] = 'false'
    os.environ['DB_RECREATE_ON_DRIFT'] = 'true'
    get_settings.cache_clear()
    reset_database_caches()

    assert initialize_database(auto_seed=True, raise_on_error=True) is True

    verify_engine = create_engine(f'sqlite:///{database_path}', future=True)
    with verify_engine.begin() as connection:
        type_row = connection.execute(text("PRAGMA table_info('social_links')")).fetchall()
        profile_column = next(row for row in type_row if row[1] == 'profile_id')
        assert profile_column[2].upper().startswith('CHAR(32)')

    session_factory = get_session_factory()
    with session_factory() as session:
        assert session.scalar(select(func.count()).select_from(Profile)) == 1
        assert session.scalar(select(func.count()).select_from(Project)) == len(PROJECT_ROWS)

    get_settings.cache_clear()
    reset_database_caches()
