from __future__ import annotations

from pydantic import Field

from app.schemas.admin_parts.common import PublicationStatusLiteral
from app.schemas.admin_parts.taxonomy import AdminBlogTagOut
from app.schemas.base import ApiSchema
from app.schemas.public import PublicMediaAssetOut


class AdminBlogPostUpsertIn(ApiSchema):
    slug: str | None = Field(default=None, max_length=160)
    title: str = Field(min_length=1, max_length=255)
    excerpt: str = Field(min_length=1)
    content_markdown: str = Field(min_length=1)
    cover_image_file_id: str | None = None
    cover_image_alt: str | None = Field(default=None, max_length=255)
    reading_time_minutes: int | None = Field(default=None, ge=0)
    status: PublicationStatusLiteral
    is_featured: bool = False
    published_at: str | None = None
    seo_title: str | None = Field(default=None, max_length=255)
    seo_description: str | None = None
    tag_ids: list[str] = Field(default_factory=list)


class AdminBlogPostOut(ApiSchema):
    id: str
    slug: str
    title: str
    excerpt: str
    content_markdown: str
    cover_image_file_id: str | None = None
    cover_image_alt: str | None = None
    cover_image: PublicMediaAssetOut | None = None
    reading_time_minutes: int | None = None
    status: PublicationStatusLiteral
    is_featured: bool
    published_at: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None
    created_at: str
    updated_at: str
    tag_ids: list[str]
    tag_names: list[str]
    tags: list[AdminBlogTagOut]


class AdminBlogPostsListOut(ApiSchema):
    items: list[AdminBlogPostOut]
    total: int


__all__ = ['AdminBlogPostOut', 'AdminBlogPostUpsertIn', 'AdminBlogPostsListOut']
