"""baseline schema

Revision ID: 20260413_0001
Revises:
Create Date: 2026-04-13 00:01:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

from app.db.types import Vector


revision = '20260413_0001'
down_revision = None
branch_labels = None
depends_on = None


event_type_enum = sa.Enum(
    'page_view',
    'portfolio_like',
    'blog_view',
    'project_click',
    'contact_submit',
    'assistant_message',
    name='eventtype',
    native_enum=False,
)
assistant_role_enum = sa.Enum('system', 'user', 'assistant', name='assistantrole', native_enum=False)
knowledge_source_type_enum = sa.Enum('profile', 'project', 'blog_post', 'experience', name='knowledgesourcetype', native_enum=False)
media_visibility_enum = sa.Enum('private', 'public', 'signed', name='mediavisibility', native_enum=False)
project_state_enum = sa.Enum('published', 'archived', 'completed', 'paused', name='projectstate', native_enum=False)
publication_status_enum = sa.Enum('draft', 'published', 'archived', name='publicationstatus', native_enum=False)


def upgrade() -> None:
    op.create_table(
        'navigation_items',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('label', sa.String(length=120), nullable=False),
        sa.Column('route_path', sa.String(length=255), nullable=False),
        sa.Column('is_external', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_visible', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'admin_users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('display_name', sa.String(length=120), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )

    op.create_table(
        'github_snapshots',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('snapshot_date', sa.Date(), nullable=False),
        sa.Column('username', sa.String(length=120), nullable=False),
        sa.Column('public_repo_count', sa.Integer(), nullable=False),
        sa.Column('followers_count', sa.Integer(), nullable=True),
        sa.Column('following_count', sa.Integer(), nullable=True),
        sa.Column('total_stars', sa.Integer(), nullable=True),
        sa.Column('total_commits', sa.Integer(), nullable=True),
        sa.Column('raw_payload', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint('public_repo_count >= 0', name='ck_github_snapshots_public_repo_count_nonnegative'),
        sa.CheckConstraint('followers_count IS NULL OR followers_count >= 0', name='ck_github_snapshots_followers_nonnegative'),
        sa.CheckConstraint('following_count IS NULL OR following_count >= 0', name='ck_github_snapshots_following_nonnegative'),
        sa.CheckConstraint('total_stars IS NULL OR total_stars >= 0', name='ck_github_snapshots_total_stars_nonnegative'),
        sa.CheckConstraint('total_commits IS NULL OR total_commits >= 0', name='ck_github_snapshots_total_commits_nonnegative'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('snapshot_date', 'username', name='uq_github_snapshots_date_username'),
    )

    op.create_table(
        'contact_messages',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('subject', sa.String(length=120), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('source_page', sa.String(length=255), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'assistant_conversations',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('session_id', sa.String(length=255), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_message_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id'),
    )

    op.create_table(
        'knowledge_documents',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('source_type', knowledge_source_type_enum, nullable=False),
        sa.Column('source_id', sa.Uuid(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('canonical_url', sa.String(length=500), nullable=True),
        sa.Column('content_markdown', sa.Text(), nullable=False),
        sa.Column('content_platform', sa.String(length=120), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'skill_categories',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    op.create_table(
        'blog_tags',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('slug', sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug'),
    )

    op.create_table(
        'media_files',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('bucket_name', sa.String(length=120), nullable=False),
        sa.Column('object_key', sa.String(length=500), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('stored_filename', sa.String(length=255), nullable=True),
        sa.Column('mime_type', sa.String(length=120), nullable=True),
        sa.Column('file_size_bytes', sa.Integer(), nullable=True),
        sa.Column('checksum', sa.String(length=255), nullable=True),
        sa.Column('public_url', sa.String(length=500), nullable=True),
        sa.Column('alt_text', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('visibility', media_visibility_enum, nullable=False),
        sa.Column('uploaded_by_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint('file_size_bytes IS NULL OR file_size_bytes >= 0', name='ck_media_files_file_size_nonnegative'),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['admin_users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('object_key', name='uq_media_files_object_key'),
    )

    op.create_table(
        'profiles',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('first_name', sa.String(length=120), nullable=False),
        sa.Column('last_name', sa.String(length=120), nullable=False),
        sa.Column('headline', sa.String(length=255), nullable=False),
        sa.Column('short_intro', sa.Text(), nullable=False),
        sa.Column('long_bio', sa.Text(), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=320), nullable=True),
        sa.Column('phone', sa.String(length=64), nullable=True),
        sa.Column('avatar_file_id', sa.Uuid(), nullable=True),
        sa.Column('hero_image_file_id', sa.Uuid(), nullable=True),
        sa.Column('resume_file_id', sa.Uuid(), nullable=True),
        sa.Column('cta_primary_label', sa.String(length=120), nullable=True),
        sa.Column('cta_primary_url', sa.String(length=500), nullable=True),
        sa.Column('cta_secondary_label', sa.String(length=120), nullable=True),
        sa.Column('cta_secondary_url', sa.String(length=500), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['avatar_file_id'], ['media_files.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['hero_image_file_id'], ['media_files.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['resume_file_id'], ['media_files.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'social_links',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('profile_id', sa.Uuid(), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('label', sa.String(length=120), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('icon_key', sa.String(length=80), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_visible', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('profile_id', 'platform', name='uq_social_links_profile_platform'),
    )

    op.create_table(
        'skills',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('category_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('years_of_experience', sa.Integer(), nullable=True),
        sa.Column('icon_key', sa.String(length=80), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_highlighted', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint('years_of_experience IS NULL OR years_of_experience >= 0', name='ck_skills_years_nonnegative'),
        sa.ForeignKeyConstraint(['category_id'], ['skill_categories.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    op.create_table(
        'experience',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organization_name', sa.String(length=255), nullable=False),
        sa.Column('role_title', sa.String(length=255), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('experience_type', sa.String(length=80), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('is_current', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('description_markdown', sa.Text(), nullable=True),
        sa.Column('logo_file_id', sa.Uuid(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['logo_file_id'], ['media_files.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'projects',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('slug', sa.String(length=160), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('teaser', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('description_markdown', sa.Text(), nullable=True),
        sa.Column('cover_image_file_id', sa.Uuid(), nullable=True),
        sa.Column('github_url', sa.String(length=500), nullable=True),
        sa.Column('github_repo_owner', sa.String(length=120), nullable=True),
        sa.Column('github_repo_name', sa.String(length=120), nullable=True),
        sa.Column('demo_url', sa.String(length=500), nullable=True),
        sa.Column('company_name', sa.String(length=255), nullable=True),
        sa.Column('started_on', sa.Date(), nullable=True),
        sa.Column('ended_on', sa.Date(), nullable=True),
        sa.Column('duration_label', sa.String(length=120), nullable=False),
        sa.Column('status', sa.String(length=120), nullable=False),
        sa.Column('state', project_state_enum, nullable=False),
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['cover_image_file_id'], ['media_files.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )

    op.create_table(
        'blog_posts',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('slug', sa.String(length=160), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('excerpt', sa.Text(), nullable=False),
        sa.Column('content_markdown', sa.Text(), nullable=False),
        sa.Column('cover_image_file_id', sa.Uuid(), nullable=True),
        sa.Column('cover_image_alt', sa.String(length=255), nullable=True),
        sa.Column('reading_time_minutes', sa.Integer(), nullable=True),
        sa.Column('status', publication_status_enum, nullable=False),
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('seo_title', sa.String(length=255), nullable=True),
        sa.Column('seo_description', sa.Text(), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['cover_image_file_id'], ['media_files.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )

    op.create_table(
        'site_events',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.Column('visitor_id', sa.String(length=255), nullable=False),
        sa.Column('page_path', sa.String(length=255), nullable=False),
        sa.Column('event_type', event_type_enum, nullable=False),
        sa.Column('referrer', sa.String(length=500), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_site_events_event_type_created_at', 'site_events', ['event_type', 'created_at'])

    op.create_table(
        'github_contribution_days',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('snapshot_id', sa.Uuid(), nullable=False),
        sa.Column('contribution_date', sa.Date(), nullable=False),
        sa.Column('contribution_count', sa.Integer(), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.CheckConstraint('contribution_count >= 0', name='ck_github_contribution_days_count_nonnegative'),
        sa.CheckConstraint('level >= 0', name='ck_github_contribution_days_level_nonnegative'),
        sa.ForeignKeyConstraint(['snapshot_id'], ['github_snapshots.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('snapshot_id', 'contribution_date', name='uq_github_contribution_days_snapshot_date'),
    )

    op.create_table(
        'assistant_messages',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('conversation_id', sa.Uuid(), nullable=False),
        sa.Column('role', assistant_role_enum, nullable=False),
        sa.Column('message_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['assistant_conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'knowledge_chunks',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('document_id', sa.Uuid(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('chunk_text', sa.Text(), nullable=False),
        sa.Column('embedding_vector', Vector(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['knowledge_documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('document_id', 'chunk_index', name='uq_knowledge_chunks_document_chunk_index'),
    )

    op.create_table(
        'experience_skills',
        sa.Column('experience_id', sa.Uuid(), nullable=False),
        sa.Column('skill_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['experience_id'], ['experience.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('experience_id', 'skill_id'),
    )

    op.create_table(
        'project_skills',
        sa.Column('project_id', sa.Uuid(), nullable=False),
        sa.Column('skill_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('project_id', 'skill_id'),
    )

    op.create_table(
        'project_images',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('project_id', sa.Uuid(), nullable=False),
        sa.Column('image_file_id', sa.Uuid(), nullable=True),
        sa.Column('alt_text', sa.String(length=255), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_cover', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(['image_file_id'], ['media_files.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'image_file_id', name='uq_project_images_project_file'),
    )

    op.create_table(
        'blog_post_tags',
        sa.Column('post_id', sa.Uuid(), nullable=False),
        sa.Column('tag_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['blog_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['blog_tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('post_id', 'tag_id'),
    )


def downgrade() -> None:
    op.drop_table('blog_post_tags')
    op.drop_table('project_images')
    op.drop_table('project_skills')
    op.drop_table('experience_skills')
    op.drop_table('knowledge_chunks')
    op.drop_table('assistant_messages')
    op.drop_table('github_contribution_days')
    op.drop_index('ix_site_events_event_type_created_at', table_name='site_events')
    op.drop_table('site_events')
    op.drop_table('blog_posts')
    op.drop_table('projects')
    op.drop_table('experience')
    op.drop_table('skills')
    op.drop_table('social_links')
    op.drop_table('profiles')
    op.drop_table('media_files')
    op.drop_table('blog_tags')
    op.drop_table('skill_categories')
    op.drop_table('knowledge_documents')
    op.drop_table('assistant_conversations')
    op.drop_table('contact_messages')
    op.drop_table('github_snapshots')
    op.drop_table('admin_users')
    op.drop_table('navigation_items')
