from __future__ import annotations

import os
from pathlib import Path
from uuid import UUID

from sqlalchemy import create_engine, func, select, text

from app.core.config import get_settings
from infra.postgres.bootstrap.bootstrap_core import initialize_database
from infra.postgres.bootstrap.seed_content import BLOG_POST_ROWS, PROFILE_ROW, PROJECT_ROWS
from infra.postgres.bootstrap.seed_ids import seed_uuid
from app.core.icon_keys import VALID_ICON_KEYS
from app.db.models import AdminUser, BlogPost, BlogTag, MediaFile, Profile, Project, ProjectSkill, Skill, SkillCategory, SocialLink
from infra.postgres.bootstrap.seed_data import MEDIA_FILES
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


def test_initialize_database_creates_and_seeds_expected_content(tmp_path: Path) -> None:
    database_path = tmp_path / 'seed.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'test-admin-pass'
    reset_database_caches()
    get_settings.cache_clear()
    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

    session_factory = get_session_factory()
    with session_factory() as session:
        assert session.scalar(select(func.count()).select_from(MediaFile)) == len(MEDIA_FILES)
        assert session.scalar(select(func.count()).select_from(Profile)) == 1
        assert session.scalar(select(func.count()).select_from(Project)) == len(PROJECT_ROWS)
        assert session.scalar(select(func.count()).select_from(BlogPost)) == len(BLOG_POST_ROWS)
        assert session.scalar(select(func.count()).select_from(SocialLink)) >= 2
        assert session.scalar(select(func.count()).select_from(ProjectSkill)) > 0
        assert session.scalar(select(func.count()).select_from(BlogTag)) > 0

        categories = session.scalars(select(SkillCategory).order_by(SkillCategory.sort_order.asc(), SkillCategory.name.asc())).all()
        assert categories
        category_icons = {category.name: category.icon_key for category in categories}
        assert category_icons['Front-End'] == 'code'
        assert category_icons['Back-End'] == 'server'
        assert category_icons['Infrastructure & Tools'] == 'database'
        assert category_icons['Languages'] == 'languages'

        profile = session.scalar(select(Profile))
        project = session.scalar(select(Project).limit(1))
        post = session.scalar(select(BlogPost).limit(1))

        assert isinstance(profile.id, UUID)
        assert isinstance(project.id, UUID)
        assert isinstance(post.id, UUID)

        assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True
        assert session.scalar(select(func.count()).select_from(Project)) == len(PROJECT_ROWS)


def test_seeded_icon_keys_use_supported_registry_values(tmp_path: Path) -> None:
    database_path = tmp_path / 'seed-icons.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    reset_database_caches()
    get_settings.cache_clear()

    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

    session_factory = get_session_factory()
    with session_factory() as session:
        category_icon_keys = {icon_key for icon_key in session.scalars(select(SkillCategory.icon_key)).all() if icon_key}
        skill_icon_keys = {icon_key for icon_key in session.scalars(select(Skill.icon_key)).all() if icon_key}
        social_icon_keys = {icon_key for icon_key in session.scalars(select(SocialLink.icon_key)).all() if icon_key}

    assert category_icon_keys <= VALID_ICON_KEYS
    assert skill_icon_keys <= VALID_ICON_KEYS
    assert social_icon_keys <= VALID_ICON_KEYS




def test_initialize_database_upserts_admin_user_for_existing_seeded_database(tmp_path: Path) -> None:
    database_path = tmp_path / 'existing-seeded.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'first-pass'
    os.environ['ADMIN_DISPLAY_NAME'] = 'First Admin'
    reset_database_caches()
    get_settings.cache_clear()

    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

    os.environ['ADMIN_EMAIL'] = 'owner@example.com'
    os.environ['ADMIN_PASSWORD'] = 'second-pass'
    os.environ['ADMIN_DISPLAY_NAME'] = 'Owner Admin'
    reset_database_caches()
    get_settings.cache_clear()

    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

    session_factory = get_session_factory()
    with session_factory() as session:
        admins = session.scalars(select(AdminUser)).all()
        assert len(admins) == 1
        assert admins[0].email == 'owner@example.com'
        assert admins[0].display_name == 'Owner Admin'


def test_initialize_database_recreates_legacy_schema_with_string_foreign_keys(tmp_path: Path) -> None:
    database_path = tmp_path / 'legacy.sqlite3'
    engine = create_engine(f'sqlite:///{database_path}', future=True)
    with engine.begin() as connection:
        connection.execute(text('CREATE TABLE profiles (id CHAR(32) PRIMARY KEY, first_name VARCHAR(120) NOT NULL, last_name VARCHAR(120) NOT NULL, headline VARCHAR(255) NOT NULL, short_intro TEXT NOT NULL, long_bio TEXT, location VARCHAR(255), email VARCHAR(320), phone VARCHAR(64), avatar_file_id CHAR(32), hero_image_file_id CHAR(32), resume_file_id CHAR(32), cta_primary_label VARCHAR(120), cta_primary_url VARCHAR(500), cta_secondary_label VARCHAR(120), cta_secondary_url VARCHAR(500), is_public BOOLEAN NOT NULL, created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL)'))
        connection.execute(text('CREATE TABLE social_links (id CHAR(32) PRIMARY KEY, profile_id VARCHAR(255) NOT NULL, platform VARCHAR(50) NOT NULL, label VARCHAR(120) NOT NULL, url VARCHAR(500) NOT NULL, icon_key VARCHAR(80), sort_order INTEGER NOT NULL, is_visible BOOLEAN NOT NULL)'))

    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    get_settings.cache_clear()
    reset_database_caches()

    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True

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
