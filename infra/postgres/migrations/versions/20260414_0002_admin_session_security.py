"""admin session security hardening

Revision ID: 20260414_0002
Revises: 20260413_0001
Create Date: 2026-04-14 00:02:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260414_0002'
down_revision = '20260413_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'admin_sessions',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('admin_user_id', sa.Uuid(), nullable=False),
        sa.Column('session_token_hash', sa.String(length=128), nullable=False),
        sa.Column('csrf_token_hash', sa.String(length=128), nullable=False),
        sa.Column('last_seen_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('revoke_reason', sa.String(length=120), nullable=True),
        sa.Column('created_ip', sa.String(length=64), nullable=True),
        sa.Column('last_seen_ip', sa.String(length=64), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['admin_user_id'], ['admin_users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_token_hash', name='uq_admin_sessions_token_hash'),
    )
    op.create_index('ix_admin_sessions_admin_user_id', 'admin_sessions', ['admin_user_id'])
    op.create_index('ix_admin_sessions_expires_at', 'admin_sessions', ['expires_at'])

    op.create_table(
        'admin_auth_events',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('admin_user_id', sa.Uuid(), nullable=True),
        sa.Column('event_type', sa.String(length=80), nullable=False),
        sa.Column('outcome', sa.String(length=40), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=True),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('session_id', sa.Uuid(), nullable=True),
        sa.Column('session_label', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['admin_user_id'], ['admin_users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['session_id'], ['admin_sessions.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_admin_auth_events_occurred_at', 'admin_auth_events', ['occurred_at'])
    op.create_index('ix_admin_auth_events_event_type_outcome', 'admin_auth_events', ['event_type', 'outcome'])


def downgrade() -> None:
    op.drop_index('ix_admin_auth_events_event_type_outcome', table_name='admin_auth_events')
    op.drop_index('ix_admin_auth_events_occurred_at', table_name='admin_auth_events')
    op.drop_table('admin_auth_events')
    op.drop_index('ix_admin_sessions_expires_at', table_name='admin_sessions')
    op.drop_index('ix_admin_sessions_admin_user_id', table_name='admin_sessions')
    op.drop_table('admin_sessions')
