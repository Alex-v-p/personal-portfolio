from __future__ import annotations

from typing import Literal

from app.schemas.base import ApiSchema

from .common import PublicMediaAssetOut


class BlogTagOut(ApiSchema):
    id: str
    name: str
    slug: str


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


class BlogPostsListOut(ApiSchema):
    items: list[BlogPostSummaryOut]
    total: int


__all__ = ['BlogPostDetailOut', 'BlogPostsListOut', 'BlogPostSummaryOut', 'BlogTagOut']
