"""add assistant-only context notes

Revision ID: 20260426_0008
Revises: 20260426_0007
Create Date: 2026-04-26 15:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260426_0008'
down_revision = '20260426_0007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'assistant_context_notes',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('title_nl', sa.String(length=255), nullable=True),
        sa.Column('content_markdown', sa.Text(), nullable=False),
        sa.Column('content_markdown_nl', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=80), nullable=False, server_default='overall_skills'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_assistant_context_notes_active_sort', 'assistant_context_notes', ['is_active', 'sort_order'])
    op.alter_column('assistant_context_notes', 'category', server_default=None)
    op.alter_column('assistant_context_notes', 'is_active', server_default=None)
    op.alter_column('assistant_context_notes', 'sort_order', server_default=None)


def downgrade() -> None:
    op.drop_index('ix_assistant_context_notes_active_sort', table_name='assistant_context_notes')
    op.drop_table('assistant_context_notes')
