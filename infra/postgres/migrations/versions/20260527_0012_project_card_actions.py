"""add project card action fields

Revision ID: 20260527_0012
Revises: 20260527_0011
Create Date: 2026-05-27 13:30:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260527_0012'
down_revision = '20260527_0011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('projects', sa.Column('read_more_url', sa.String(length=500), nullable=True))
    op.add_column('projects', sa.Column('read_more_url_nl', sa.String(length=500), nullable=True))
    op.add_column(
        'projects',
        sa.Column('is_card_popup_enabled', sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column('projects', 'is_card_popup_enabled')
    op.drop_column('projects', 'read_more_url_nl')
    op.drop_column('projects', 'read_more_url')
