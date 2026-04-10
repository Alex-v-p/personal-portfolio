from __future__ import annotations

from typing import Literal

from app.schemas.base import ApiSchema


class HeroActionOut(ApiSchema):
    label: str
    appearance: Literal['primary', 'secondary', 'ghost']
    href: str | None = None
    router_link: str | list[str] | None = None
    open_in_new_tab: bool | None = None


class ExpertiseGroupOut(ApiSchema):
    title: str
    tags: list[str]


class ProfileOut(ApiSchema):
    id: str
    first_name: str
    last_name: str
    name: str
    headline: str
    role: str
    greeting: str
    location: str
    email: str
    phone: str
    short_intro: str
    long_bio: str
    hero_title: str
    summary: str
    short_bio: str
    footer_description: str
    avatar_file_id: str | None = None
    hero_image_file_id: str | None = None
    resume_file_id: str | None = None
    avatar_url: str | None = None
    hero_image_url: str | None = None
    resume_url: str | None = None
    skills: list[str]
    expertise_groups: list[ExpertiseGroupOut]
    intro_paragraphs: list[str]
    availability: list[str]
    hero_actions: list[HeroActionOut]
    created_at: str | None = None
    updated_at: str | None = None


class ProjectLinkOut(ApiSchema):
    label: str
    href: str | None = None
    router_link: str | list[str] | None = None


class ProjectOut(ApiSchema):
    id: str
    slug: str
    title: str
    teaser: str
    short_description: str
    summary: str
    description_markdown: str | None = None
    organization: str
    duration: str
    duration_label: str
    status: str
    state: Literal['published', 'archived', 'completed', 'paused']
    category: str
    tags: list[str]
    featured: bool
    is_featured: bool
    image_alt: str
    cover_image_alt: str
    cover_image_file_id: str | None = None
    cover_image_url: str | None = None
    highlight: str
    github_url: str | None = None
    github_repo_name: str | None = None
    demo_url: str | None = None
    started_on: str | None = None
    ended_on: str | None = None
    published_at: str | None = None
    sort_order: int
    links: list[ProjectLinkOut]


class ProjectsListOut(ApiSchema):
    items: list[ProjectOut]
    total: int


class BlogPostOut(ApiSchema):
    id: str
    slug: str
    title: str
    excerpt: str
    published_at: str
    read_time: str
    reading_time_minutes: int
    category: str
    tags: list[str]
    featured: bool
    is_featured: bool
    cover_alt: str
    cover_image_alt: str
    cover_image_file_id: str | None = None
    cover_image_url: str | None = None
    status: Literal['draft', 'published', 'archived']
    content_markdown: str
    seo_title: str | None = None
    seo_description: str | None = None


class BlogPostsListOut(ApiSchema):
    items: list[BlogPostOut]
    total: int
