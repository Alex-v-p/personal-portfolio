"""add dutch locale columns for public content

Revision ID: 20260421_0004
Revises: 20260414_0003
Create Date: 2026-04-21 00:04:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260421_0004'
down_revision = '20260414_0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('profiles') as batch_op:
        batch_op.add_column(sa.Column('headline_nl', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('short_intro_nl', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('long_bio_nl', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('cta_primary_label_nl', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('cta_secondary_label_nl', sa.String(length=120), nullable=True))

    with op.batch_alter_table('navigation_items') as batch_op:
        batch_op.add_column(sa.Column('label_nl', sa.String(length=120), nullable=True))

    with op.batch_alter_table('projects') as batch_op:
        batch_op.add_column(sa.Column('title_nl', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('teaser_nl', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('summary_nl', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('description_markdown_nl', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('duration_label_nl', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('status_nl', sa.String(length=120), nullable=True))

    with op.batch_alter_table('project_images') as batch_op:
        batch_op.add_column(sa.Column('alt_text_nl', sa.String(length=255), nullable=True))

    with op.batch_alter_table('blog_posts') as batch_op:
        batch_op.add_column(sa.Column('title_nl', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('excerpt_nl', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('content_markdown_nl', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('cover_image_alt_nl', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('seo_title_nl', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('seo_description_nl', sa.Text(), nullable=True))

    with op.batch_alter_table('experience') as batch_op:
        batch_op.add_column(sa.Column('role_title_nl', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('summary_nl', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('description_markdown_nl', sa.Text(), nullable=True))

    with op.batch_alter_table('skill_categories') as batch_op:
        batch_op.add_column(sa.Column('name_nl', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('description_nl', sa.Text(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('skill_categories') as batch_op:
        batch_op.drop_column('description_nl')
        batch_op.drop_column('name_nl')

    with op.batch_alter_table('experience') as batch_op:
        batch_op.drop_column('description_markdown_nl')
        batch_op.drop_column('summary_nl')
        batch_op.drop_column('role_title_nl')

    with op.batch_alter_table('blog_posts') as batch_op:
        batch_op.drop_column('seo_description_nl')
        batch_op.drop_column('seo_title_nl')
        batch_op.drop_column('cover_image_alt_nl')
        batch_op.drop_column('content_markdown_nl')
        batch_op.drop_column('excerpt_nl')
        batch_op.drop_column('title_nl')

    with op.batch_alter_table('project_images') as batch_op:
        batch_op.drop_column('alt_text_nl')

    with op.batch_alter_table('projects') as batch_op:
        batch_op.drop_column('status_nl')
        batch_op.drop_column('duration_label_nl')
        batch_op.drop_column('description_markdown_nl')
        batch_op.drop_column('summary_nl')
        batch_op.drop_column('teaser_nl')
        batch_op.drop_column('title_nl')

    with op.batch_alter_table('navigation_items') as batch_op:
        batch_op.drop_column('label_nl')

    with op.batch_alter_table('profiles') as batch_op:
        batch_op.drop_column('cta_secondary_label_nl')
        batch_op.drop_column('cta_primary_label_nl')
        batch_op.drop_column('long_bio_nl')
        batch_op.drop_column('short_intro_nl')
        batch_op.drop_column('headline_nl')
