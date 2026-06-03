"""add visibility toggle for experience entries

Revision ID: 20260603_0014
Revises: 20260527_0013
Create Date: 2026-06-03 21:35:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260603_0014'
down_revision = '20260527_0013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('experience') as batch_op:
        batch_op.add_column(sa.Column('is_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade() -> None:
    with op.batch_alter_table('experience') as batch_op:
        batch_op.drop_column('is_enabled')
