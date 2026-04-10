from __future__ import annotations

from typing import Literal

from app.schemas.base import ApiSchema


class SocialLinkOut(ApiSchema):
    id: str
    profile_id: str
    platform: str
    label: str
    url: str
    icon_key: str | None = None
    sort_order: int
    is_visible: bool


class ProfileOut(ApiSchema):
    id: str
    first_name: str
    last_name: str
    headline: str
    short_intro: str
    long_bio: str | None = None
    location: str | None = None
    email: str | None = None
    phone: str | None = None
    avatar_file_id: str | None = None
    hero_image_file_id: str | None = None
    resume_file_id: str | None = None
    cta_primary_label: str | None = None
    cta_primary_url: str | None = None
    cta_secondary_label: str | None = None
    cta_secondary_url: str | None = None
    is_public: bool
    social_links: list[SocialLinkOut]
    created_at: str
    updated_at: str


class SkillSummaryOut(ApiSchema):
    id: str
    category_id: str
    name: str
    years_of_experience: int | None = None
    icon_key: str | None = None
    sort_order: int
    is_highlighted: bool


class ProjectImageOut(ApiSchema):
    id: str
    project_id: str
    image_file_id: str | None = None
    alt_text: str | None = None
    sort_order: int
    is_cover: bool


class ProjectOut(ApiSchema):
    id: str
    slug: str
    title: str
    teaser: str
    summary: str | None = None
    description_markdown: str | None = None
    cover_image_file_id: str | None = None
    github_url: str | None = None
    github_repo_owner: str | None = None
    github_repo_name: str | None = None
    demo_url: str | None = None
    company_name: str | None = None
    started_on: str | None = None
    ended_on: str | None = None
    duration_label: str
    status: str
    state: Literal['published', 'archived', 'completed', 'paused']
    is_featured: bool
    sort_order: int
    published_at: str
    created_at: str
    updated_at: str
    skills: list[SkillSummaryOut]
    images: list[ProjectImageOut]


class ProjectsListOut(ApiSchema):
    items: list[ProjectOut]
    total: int


class BlogTagOut(ApiSchema):
    id: str
    name: str
    slug: str


class BlogPostOut(ApiSchema):
    id: str
    slug: str
    title: str
    excerpt: str
    content_markdown: str
    cover_image_file_id: str | None = None
    cover_image_alt: str | None = None
    reading_time_minutes: int | None = None
    status: Literal['draft', 'published', 'archived']
    is_featured: bool
    published_at: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None
    created_at: str
    updated_at: str
    tags: list[BlogTagOut]


class BlogPostsListOut(ApiSchema):
    items: list[BlogPostOut]
    total: int
