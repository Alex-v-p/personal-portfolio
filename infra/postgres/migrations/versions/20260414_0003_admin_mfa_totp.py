"""admin mfa totp rollout

Revision ID: 20260414_0003
Revises: 20260414_0002
Create Date: 2026-04-14 00:03:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260414_0003'
down_revision = '20260414_0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('admin_users') as batch_op:
        batch_op.add_column(sa.Column('mfa_enabled', sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column('mfa_totp_secret_encrypted', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('mfa_enrolled_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('mfa_recovery_codes_hashes', sa.JSON(), nullable=True))

    with op.batch_alter_table('admin_sessions') as batch_op:
        batch_op.add_column(sa.Column('mfa_completed_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('mfa_pending_secret_encrypted', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('mfa_pending_created_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('admin_sessions') as batch_op:
        batch_op.drop_column('mfa_pending_created_at')
        batch_op.drop_column('mfa_pending_secret_encrypted')
        batch_op.drop_column('mfa_completed_at')

    with op.batch_alter_table('admin_users') as batch_op:
        batch_op.drop_column('mfa_recovery_codes_hashes')
        batch_op.drop_column('mfa_enrolled_at')
        batch_op.drop_column('mfa_totp_secret_encrypted')
        batch_op.drop_column('mfa_enabled')
