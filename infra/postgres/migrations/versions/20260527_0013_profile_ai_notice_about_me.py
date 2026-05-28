"""add profile AI notice columns

Revision ID: 20260527_0013
Revises: 20260527_0012
Create Date: 2026-05-27 15:45:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260527_0013'
down_revision = '20260527_0012'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('profiles', sa.Column('ai_notice', sa.Text(), nullable=True))
    op.add_column('profiles', sa.Column('ai_notice_nl', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('profiles', 'ai_notice_nl')
    op.drop_column('profiles', 'ai_notice')
