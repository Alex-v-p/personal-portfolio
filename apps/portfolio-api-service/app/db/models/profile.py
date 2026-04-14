from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.media import MediaFile


class Profile(TimestampMixin, Base):
    __tablename__ = 'profiles'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    headline: Mapped[str] = mapped_column(String(255), nullable=False)
    short_intro: Mapped[str] = mapped_column(Text, nullable=False)
    long_bio: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(320))
    phone: Mapped[str | None] = mapped_column(String(64))
    avatar_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    hero_image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    resume_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    cta_primary_label: Mapped[str | None] = mapped_column(String(120))
    cta_primary_url: Mapped[str | None] = mapped_column(String(500))
    cta_secondary_label: Mapped[str | None] = mapped_column(String(120))
    cta_secondary_url: Mapped[str | None] = mapped_column(String(500))
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    avatar_file: Mapped[MediaFile | None] = relationship(
        'MediaFile',
        foreign_keys='Profile.avatar_file_id',
        back_populates='profile_avatar_for',
    )
    hero_image_file: Mapped[MediaFile | None] = relationship(
        'MediaFile',
        foreign_keys='Profile.hero_image_file_id',
        back_populates='profile_hero_for',
    )
    resume_file: Mapped[MediaFile | None] = relationship(
        'MediaFile',
        foreign_keys='Profile.resume_file_id',
        back_populates='profile_resume_for',
    )
    social_links: Mapped[list[SocialLink]] = relationship(
        back_populates='profile', cascade='all, delete-orphan', order_by='SocialLink.sort_order'
    )


class SocialLink(Base):
    __tablename__ = 'social_links'
    __table_args__ = (
        UniqueConstraint('profile_id', 'platform', name='uq_social_links_profile_platform'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    profile_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    icon_key: Mapped[str | None] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    profile: Mapped[Profile] = relationship(back_populates='social_links')
