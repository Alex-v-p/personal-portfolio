from __future__ import annotations

from pydantic import Field

from app.schemas.admin_parts.common import ProjectStateLiteral, PublicationStatusLiteral
from app.schemas.base import ApiSchema
from app.schemas.public import PublicMediaAssetOut, SkillSummaryOut
from app.schemas.admin_parts.taxonomy import AdminBlogTagOut


class AdminProjectUpsertIn(ApiSchema):
    slug: str | None = Field(default=None, max_length=160)
    title: str = Field(min_length=1, max_length=255)
    teaser: str = Field(min_length=1)
    summary: str | None = None
    description_markdown: str | None = None
    cover_image_file_id: str | None = None
    github_url: str | None = Field(default=None, max_length=500)
    github_repo_owner: str | None = Field(default=None, max_length=120)
    github_repo_name: str | None = Field(default=None, max_length=120)
    demo_url: str | None = Field(default=None, max_length=500)
    company_name: str | None = Field(default=None, max_length=255)
    started_on: str | None = None
    ended_on: str | None = None
    duration_label: str = Field(min_length=1, max_length=120)
    status: str = Field(min_length=1, max_length=120)
    state: ProjectStateLiteral
    is_featured: bool = False
    sort_order: int = 0
    published_at: str | None = None
    skill_ids: list[str] = Field(default_factory=list)


class AdminProjectOut(ApiSchema):
    id: str
    slug: str
    title: str
    teaser: str
    summary: str | None = None
    description_markdown: str | None = None
    cover_image_file_id: str | None = None
    cover_image: PublicMediaAssetOut | None = None
    github_url: str | None = None
    github_repo_owner: str | None = None
    github_repo_name: str | None = None
    demo_url: str | None = None
    company_name: str | None = None
    started_on: str | None = None
    ended_on: str | None = None
    duration_label: str
    status: str
    state: ProjectStateLiteral
    is_featured: bool
    sort_order: int
    published_at: str
    created_at: str
    updated_at: str
    skill_ids: list[str]
    skills: list[SkillSummaryOut]


class AdminProjectsListOut(ApiSchema):
    items: list[AdminProjectOut]
    total: int


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


class AdminExperienceUpsertIn(ApiSchema):
    organization_name: str = Field(min_length=1, max_length=255)
    role_title: str = Field(min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    experience_type: str = Field(min_length=1, max_length=80)
    start_date: str
    end_date: str | None = None
    is_current: bool = False
    summary: str = Field(min_length=1)
    description_markdown: str | None = None
    logo_file_id: str | None = None
    sort_order: int = 0
    skill_ids: list[str] = Field(default_factory=list)


class AdminExperienceOut(ApiSchema):
    id: str
    organization_name: str
    role_title: str
    location: str | None = None
    experience_type: str
    start_date: str
    end_date: str | None = None
    is_current: bool
    summary: str
    description_markdown: str | None = None
    logo_file_id: str | None = None
    logo: PublicMediaAssetOut | None = None
    sort_order: int
    created_at: str
    updated_at: str
    skill_ids: list[str]
    skills: list[SkillSummaryOut]


class AdminExperiencesListOut(ApiSchema):
    items: list[AdminExperienceOut]
    total: int


__all__ = [
    'AdminBlogPostOut',
    'AdminBlogPostUpsertIn',
    'AdminBlogPostsListOut',
    'AdminExperienceOut',
    'AdminExperienceUpsertIn',
    'AdminExperiencesListOut',
    'AdminProjectOut',
    'AdminProjectUpsertIn',
    'AdminProjectsListOut',
]
