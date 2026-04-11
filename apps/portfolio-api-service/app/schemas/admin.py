from __future__ import annotations

from typing import Literal

from pydantic import EmailStr, Field

from app.schemas.base import ApiSchema
from app.schemas.public import PublicMediaAssetOut, SkillSummaryOut

ProjectStateLiteral = Literal['published', 'archived', 'completed', 'paused']
PublicationStatusLiteral = Literal['draft', 'published', 'archived']


class AdminUserOut(ApiSchema):
    id: str
    email: str
    display_name: str
    is_active: bool
    created_at: str


class AdminAuthTokenOut(ApiSchema):
    access_token: str
    token_type: str = 'bearer'
    expires_in_seconds: int
    user: AdminUserOut


class AdminLoginIn(ApiSchema):
    email: EmailStr
    password: str


class AdminMediaFileOut(ApiSchema):
    id: str
    bucket_name: str
    object_key: str
    original_filename: str
    mime_type: str | None = None
    visibility: str
    alt_text: str | None = None
    title: str | None = None
    public_url: str | None = None
    resolved_asset: PublicMediaAssetOut | None = None
    created_at: str
    updated_at: str


class AdminSocialLinkIn(ApiSchema):
    id: str | None = None
    platform: str = Field(min_length=1, max_length=50)
    label: str = Field(min_length=1, max_length=120)
    url: str = Field(min_length=1, max_length=500)
    icon_key: str | None = Field(default=None, max_length=80)
    sort_order: int = 0
    is_visible: bool = True


class AdminProfileUpdateIn(ApiSchema):
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    headline: str = Field(min_length=1, max_length=255)
    short_intro: str = Field(min_length=1)
    long_bio: str | None = None
    location: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=64)
    avatar_file_id: str | None = None
    hero_image_file_id: str | None = None
    resume_file_id: str | None = None
    cta_primary_label: str | None = Field(default=None, max_length=120)
    cta_primary_url: str | None = Field(default=None, max_length=500)
    cta_secondary_label: str | None = Field(default=None, max_length=120)
    cta_secondary_url: str | None = Field(default=None, max_length=500)
    is_public: bool = True
    social_links: list[AdminSocialLinkIn] = Field(default_factory=list)


class AdminSocialLinkOut(ApiSchema):
    id: str
    platform: str
    label: str
    url: str
    icon_key: str | None = None
    sort_order: int
    is_visible: bool


class AdminProfileOut(ApiSchema):
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
    avatar: PublicMediaAssetOut | None = None
    hero_image: PublicMediaAssetOut | None = None
    resume: PublicMediaAssetOut | None = None
    cta_primary_label: str | None = None
    cta_primary_url: str | None = None
    cta_secondary_label: str | None = None
    cta_secondary_url: str | None = None
    is_public: bool
    social_links: list[AdminSocialLinkOut]
    created_at: str
    updated_at: str


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
    tag_names: list[str] = Field(default_factory=list)


class AdminBlogTagOut(ApiSchema):
    id: str
    name: str
    slug: str


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
    tag_names: list[str]
    tags: list[AdminBlogTagOut]


class AdminBlogPostsListOut(ApiSchema):
    items: list[AdminBlogPostOut]
    total: int


class AdminContactMessageOut(ApiSchema):
    id: str
    name: str
    email: str
    subject: str
    message: str
    source_page: str
    is_read: bool
    created_at: str
    updated_at: str


class AdminContactMessagesListOut(ApiSchema):
    items: list[AdminContactMessageOut]
    total: int


class AdminMessageStatusUpdateIn(ApiSchema):
    is_read: bool


class AdminReferenceDataOut(ApiSchema):
    skills: list[SkillSummaryOut]
    media_files: list[AdminMediaFileOut]
    blog_tags: list[AdminBlogTagOut]
    project_states: list[ProjectStateLiteral]
    publication_statuses: list[PublicationStatusLiteral]


class AdminDashboardSummaryOut(ApiSchema):
    projects: int
    blog_posts: int
    unread_messages: int
    skills: int
    media_files: int
