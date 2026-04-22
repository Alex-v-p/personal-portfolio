"""add icon key to skill categories

Revision ID: 20260422_0005
Revises: 20260421_0004
Create Date: 2026-04-22 00:05:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260422_0005'
down_revision = '20260421_0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('skill_categories') as batch_op:
        batch_op.add_column(sa.Column('icon_key', sa.String(length=80), nullable=True))

    category_icon_keys = {
        'Front-End': 'code',
        'Back-End': 'server',
        'Data & AI': 'brain',
        'Infrastructure & Tools': 'database',
        'Analysis & Collaboration': 'workflow',
        'Languages': 'languages',
    }
    categories_table = sa.table(
        'skill_categories',
        sa.column('name', sa.String(length=120)),
        sa.column('icon_key', sa.String(length=80)),
    )
    for name, icon_key in category_icon_keys.items():
        op.execute(
            categories_table.update()
            .where(categories_table.c.name == name)
            .values(icon_key=icon_key)
        )


def downgrade() -> None:
    with op.batch_alter_table('skill_categories') as batch_op:
        batch_op.drop_column('icon_key')
