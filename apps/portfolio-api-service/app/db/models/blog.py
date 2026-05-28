from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
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
    title_nl: Mapped[str | None] = mapped_column(String(255))
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt_nl: Mapped[str | None] = mapped_column(Text)
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    content_markdown_nl: Mapped[str | None] = mapped_column(Text)
    cover_image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    cover_image_alt: Mapped[str | None] = mapped_column(String(255))
    cover_image_alt_nl: Mapped[str | None] = mapped_column(String(255))
    reading_time_minutes: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[PublicationStatus] = mapped_column(SqlEnum(PublicationStatus, native_enum=False), nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    seo_title: Mapped[str | None] = mapped_column(String(255))
    seo_title_nl: Mapped[str | None] = mapped_column(String(255))
    seo_description: Mapped[str | None] = mapped_column(Text)
    seo_description_nl: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    cover_image_file: Mapped[MediaFile | None] = relationship(
        'MediaFile',
        foreign_keys='BlogPost.cover_image_file_id',
        back_populates='blog_cover_for',
    )
    tag_links: Mapped[list[BlogPostTag]] = relationship(back_populates='post', cascade='all, delete-orphan')
    protected_document_groups: Mapped[list[BlogProtectedDocumentGroup]] = relationship(
        back_populates='blog_post',
        cascade='all, delete-orphan',
        order_by='BlogProtectedDocumentGroup.sort_order',
    )


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


class BlogProtectedDocumentGroup(TimestampMixin, Base):
    __tablename__ = 'blog_protected_document_groups'
    __table_args__ = (
        UniqueConstraint('slug', name='uq_blog_protected_document_groups_slug'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    blog_post_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('blog_posts.id', ondelete='CASCADE'), nullable=False)
    slug: Mapped[str] = mapped_column(String(160), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    title_nl: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    description_nl: Mapped[str | None] = mapped_column(Text)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    blog_post: Mapped[BlogPost] = relationship(back_populates='protected_document_groups')
    documents: Mapped[list[BlogProtectedDocument]] = relationship(
        back_populates='group',
        cascade='all, delete-orphan',
        order_by='BlogProtectedDocument.sort_order',
    )


class BlogProtectedDocument(TimestampMixin, Base):
    __tablename__ = 'blog_protected_documents'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    group_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('blog_protected_document_groups.id', ondelete='CASCADE'), nullable=False)
    media_file_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='RESTRICT'), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255))
    title_nl: Mapped[str | None] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    group: Mapped[BlogProtectedDocumentGroup] = relationship(back_populates='documents')
    media_file: Mapped[MediaFile] = relationship('MediaFile', back_populates='protected_blog_documents')
