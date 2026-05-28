"""add short-lived assistant conversation summaries

Revision ID: 20260426_0010
Revises: 20260426_0009
Create Date: 2026-04-26 17:30:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260426_0010'
down_revision = '20260426_0009'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('assistant_conversations', sa.Column('conversation_summary', sa.Text(), nullable=True))
    op.add_column(
        'assistant_conversations',
        sa.Column('summary_message_count', sa.Integer(), nullable=False, server_default='0'),
    )
    op.add_column('assistant_conversations', sa.Column('summary_updated_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('assistant_conversations', 'summary_updated_at')
    op.drop_column('assistant_conversations', 'summary_message_count')
    op.drop_column('assistant_conversations', 'conversation_summary')
