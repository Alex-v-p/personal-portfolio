from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import PublicationStatus

if TYPE_CHECKING:
    from app.db.models.media import MediaFile


class BlogPost(TimestampMixin, Base):
    __tablename__ = 'blog_posts'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    cover_image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    cover_image_alt: Mapped[str | None] = mapped_column(String(255))
    reading_time_minutes: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[PublicationStatus] = mapped_column(SqlEnum(PublicationStatus, native_enum=False), nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    seo_title: Mapped[str | None] = mapped_column(String(255))
    seo_description: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    cover_image_file: Mapped[MediaFile | None] = relationship(
        'MediaFile',
        foreign_keys='BlogPost.cover_image_file_id',
        back_populates='blog_cover_for',
    )
    tag_links: Mapped[list[BlogPostTag]] = relationship(back_populates='post', cascade='all, delete-orphan')


class BlogTag(Base):
    __tablename__ = 'blog_tags'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

    post_links: Mapped[list[BlogPostTag]] = relationship(back_populates='tag', cascade='all, delete-orphan')


class BlogPostTag(Base):
    __tablename__ = 'blog_post_tags'

    post_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('blog_posts.id', ondelete='CASCADE'), primary_key=True
    )
    tag_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('blog_tags.id', ondelete='CASCADE'), primary_key=True
    )

    post: Mapped[BlogPost] = relationship(back_populates='tag_links')
    tag: Mapped[BlogTag] = relationship(back_populates='post_links')
