from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.schemas.base import ApiSchema

from .common import PublicMediaAssetOut


class BlogTagOut(ApiSchema):
    id: str
    name: str
    slug: str


class ProtectedDocumentOut(ApiSchema):
    id: str
    title: str
    file_name: str | None = None
    mime_type: str | None = None
    file_size_bytes: int | None = None
    download_url: str


class ProtectedDocumentGroupOut(ApiSchema):
    slug: str
    title: str
    description: str | None = None
    documents: list[ProtectedDocumentOut] = Field(default_factory=list)


class ProtectedDocumentsUnlockIn(ApiSchema):
    password: str


class ProtectedDocumentsAccessOut(ApiSchema):
    unlocked: bool
    expires_in_seconds: int = 0


class ProtectedDocumentsUnlockOut(ProtectedDocumentsAccessOut):
    pass


class BlogPostSummaryOut(ApiSchema):
    id: str
    slug: str
    title: str
    excerpt: str
    cover_image_file_id: str | None = None
    cover_image_alt: str | None = None
    cover_image: PublicMediaAssetOut | None = None
    reading_time_minutes: int | None = None
    status: Literal['draft', 'published', 'archived']
    is_featured: bool
    published_at: str | None = None
    created_at: str
    updated_at: str
    tags: list[BlogTagOut]


class BlogPostDetailOut(BlogPostSummaryOut):
    content_markdown: str
    seo_title: str | None = None
    seo_description: str | None = None
    protected_document_groups: list[ProtectedDocumentGroupOut] = Field(default_factory=list)


class BlogPostsListOut(ApiSchema):
    items: list[BlogPostSummaryOut]
    total: int


__all__ = [
    'BlogPostDetailOut',
    'BlogPostsListOut',
    'BlogPostSummaryOut',
    'BlogTagOut',
    'ProtectedDocumentGroupOut',
    'ProtectedDocumentOut',
    'ProtectedDocumentsAccessOut',
    'ProtectedDocumentsUnlockIn',
    'ProtectedDocumentsUnlockOut',
]
