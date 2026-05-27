"""add CMS-managed protected blog documents

Revision ID: 20260527_0011
Revises: 20260426_0010
Create Date: 2026-05-27 06:20:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260527_0011'
down_revision = '20260426_0010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'blog_protected_document_groups',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('blog_post_id', sa.Uuid(), nullable=False),
        sa.Column('slug', sa.String(length=160), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('title_nl', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_nl', sa.Text(), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['blog_post_id'], ['blog_posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug', name='uq_blog_protected_document_groups_slug'),
    )

    op.create_table(
        'blog_protected_documents',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('group_id', sa.Uuid(), nullable=False),
        sa.Column('media_file_id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('title_nl', sa.String(length=255), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['blog_protected_document_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['media_file_id'], ['media_files.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index('ix_blog_protected_document_groups_blog_post_id', 'blog_protected_document_groups', ['blog_post_id'])
    op.create_index('ix_blog_protected_documents_group_id', 'blog_protected_documents', ['group_id'])
    op.create_index('ix_blog_protected_documents_media_file_id', 'blog_protected_documents', ['media_file_id'])


def downgrade() -> None:
    op.drop_index('ix_blog_protected_documents_media_file_id', table_name='blog_protected_documents')
    op.drop_index('ix_blog_protected_documents_group_id', table_name='blog_protected_documents')
    op.drop_index('ix_blog_protected_document_groups_blog_post_id', table_name='blog_protected_document_groups')
    op.drop_table('blog_protected_documents')
    op.drop_table('blog_protected_document_groups')
