from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.media import MediaFile


class AdminUser(TimestampMixin, Base):
    __tablename__ = 'admin_users'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    uploaded_media_files: Mapped[list[MediaFile]] = relationship(back_populates='uploaded_by')
    sessions: Mapped[list[AdminSession]] = relationship(back_populates='admin_user', cascade='all, delete-orphan')
    auth_events: Mapped[list[AdminAuthEvent]] = relationship(back_populates='admin_user', cascade='all, delete-orphan')


class AdminSession(TimestampMixin, Base):
    __tablename__ = 'admin_sessions'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    admin_user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('admin_users.id', ondelete='CASCADE'), nullable=False)
    session_token_hash: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    csrf_token_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoke_reason: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_seen_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)

    admin_user: Mapped[AdminUser] = relationship(back_populates='sessions')


class AdminAuthEvent(Base):
    __tablename__ = 'admin_auth_events'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    admin_user_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('admin_users.id', ondelete='SET NULL'), nullable=True)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    outcome: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    session_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('admin_sessions.id', ondelete='SET NULL'), nullable=True)
    session_label: Mapped[str | None] = mapped_column(Text, nullable=True)

    admin_user: Mapped[AdminUser | None] = relationship(back_populates='auth_events')
