"""expand knowledge document source type length

Revision ID: 20260426_0009
Revises: 20260426_0008
Create Date: 2026-04-26 16:05:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260426_0009'
down_revision = '20260426_0008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLAlchemy's non-native Enum used the maximum length of the original
    # enum names (10 chars: EXPERIENCE). The new ASSISTANT_NOTE enum name is
    # longer, so widen the storage column before assistant-only notes are
    # indexed into knowledge_documents.
    op.alter_column(
        'knowledge_documents',
        'source_type',
        existing_type=sa.String(length=10),
        type_=sa.String(length=32),
        existing_nullable=False,
    )


def downgrade() -> None:
    # Remove assistant-note documents first so shrinking the column cannot fail.
    op.execute("DELETE FROM knowledge_chunks WHERE metadata ->> 'source_type' = 'assistant_note'")
    op.execute("DELETE FROM knowledge_documents WHERE source_type = 'ASSISTANT_NOTE'")
    op.alter_column(
        'knowledge_documents',
        'source_type',
        existing_type=sa.String(length=32),
        type_=sa.String(length=10),
        existing_nullable=False,
    )
