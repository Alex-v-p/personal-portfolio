from __future__ import annotations

from typing import Literal

from app.schemas.base import ApiSchema


class PublicMediaAssetOut(ApiSchema):
    id: str
    url: str
    alt: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    width: int | None = None
    height: int | None = None


class SocialLinkOut(ApiSchema):
    id: str
    profile_id: str
    platform: str
    label: str
    url: str
    icon_key: str | None = None
    sort_order: int
    is_visible: bool


class NavigationItemOut(ApiSchema):
    id: str
    label: str
    route_path: str
    is_external: bool
    sort_order: int
    is_visible: bool


class NavigationListOut(ApiSchema):
    items: list[NavigationItemOut]
    total: int


class SkillSummaryOut(ApiSchema):
    id: str
    category_id: str
    name: str
    years_of_experience: int | None = None
    icon_key: str | None = None
    sort_order: int
    is_highlighted: bool


class ExpertiseGroupOut(ApiSchema):
    title: str
    tags: list[str]


class ContactMethodOut(ApiSchema):
    id: str
    platform: str
    label: str
    value: str
    href: str
    action_label: str
    icon_key: str | None = None
    description: str | None = None
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
    avatar: PublicMediaAssetOut | None = None
    hero_image: PublicMediaAssetOut | None = None
    resume: PublicMediaAssetOut | None = None
    cta_primary_label: str | None = None
    cta_primary_url: str | None = None
    cta_secondary_label: str | None = None
    cta_secondary_url: str | None = None
    is_public: bool
    social_links: list[SocialLinkOut]
    footer_description: str
    intro_paragraphs: list[str]
    availability: list[str]
    skills: list[str]
    expertise_groups: list[ExpertiseGroupOut]
    created_at: str
    updated_at: str


class ProjectImageOut(ApiSchema):
    id: str
    project_id: str
    image_file_id: str | None = None
    alt_text: str | None = None
    sort_order: int
    is_cover: bool
    image: PublicMediaAssetOut | None = None


class ProjectSummaryOut(ApiSchema):
    id: str
    slug: str
    title: str
    teaser: str
    summary: str | None = None
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
    state: Literal['published', 'archived', 'completed', 'paused']
    is_featured: bool
    sort_order: int
    published_at: str
    created_at: str
    updated_at: str
    skills: list[SkillSummaryOut]


class ProjectDetailOut(ProjectSummaryOut):
    description_markdown: str | None = None
    images: list[ProjectImageOut]


class ProjectsListOut(ApiSchema):
    items: list[ProjectSummaryOut]
    total: int


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


class ExperienceOut(ApiSchema):
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
    skill_names: list[str]
    created_at: str
    updated_at: str


class ExperienceListOut(ApiSchema):
    items: list[ExperienceOut]
    total: int


class SiteShellOut(ApiSchema):
    navigation: NavigationListOut
    profile: ProfileOut
    footer_text: str
    contact_methods: list[ContactMethodOut]


class HomeOut(ApiSchema):
    hero: ProfileOut
    featured_projects: list[ProjectSummaryOut]
    featured_blog_posts: list[BlogPostSummaryOut]
    expertise_groups: list[ExpertiseGroupOut]
    experience_preview: list[ExperienceOut]
    contact_preview: list[ContactMethodOut]


class StatItemOut(ApiSchema):
    id: str
    label: str
    value: str
    description: str
    action_label: str | None = None
    meta: str | None = None
    footnote: str | None = None


class GithubContributionDayOut(ApiSchema):
    date: str
    count: int
    level: int


class GithubSnapshotOut(ApiSchema):
    id: str
    snapshot_date: str
    username: str
    public_repo_count: int
    followers_count: int | None = None
    following_count: int | None = None
    total_stars: int | None = None
    total_commits: int | None = None
    created_at: str
    contribution_days: list[GithubContributionDayOut]


class StatsOut(ApiSchema):
    contribution_weeks: list[list[int]]
    github_summary: StatItemOut
    latest_github_snapshot: GithubSnapshotOut | None = None
    portfolio_highlights: list[StatItemOut]
    portfolio_stats: list[StatItemOut]
    month_labels: list[str]
    weekday_labels: list[str]
