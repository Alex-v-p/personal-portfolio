from __future__ import annotations

from typing import Any, Literal

from pydantic import EmailStr, Field

from app.schemas.base import ApiSchema
from app.schemas.public import PublicMediaAssetOut, SkillSummaryOut

ProjectStateLiteral = Literal['published', 'archived', 'completed', 'paused']
PublicationStatusLiteral = Literal['draft', 'published', 'archived']
MediaVisibilityLiteral = Literal['public', 'private', 'signed']


class AdminUserOut(ApiSchema):
    id: str
    email: str
    display_name: str
    is_active: bool
    created_at: str


class AdminUserCreateIn(ApiSchema):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=255)
    is_active: bool = True


class AdminUserUpdateIn(ApiSchema):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=120)
    password: str | None = Field(default=None, min_length=8, max_length=255)
    is_active: bool = True


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


class AdminMediaUploadOut(AdminMediaFileOut):
    pass


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


class AdminSkillCategoryOut(ApiSchema):
    id: str
    name: str
    description: str | None = None
    sort_order: int


class AdminSkillCategoryUpsertIn(ApiSchema):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    sort_order: int = 0


class AdminSkillOut(ApiSchema):
    id: str
    category_id: str
    name: str
    years_of_experience: int | None = None
    icon_key: str | None = None
    sort_order: int
    is_highlighted: bool


class AdminSkillUpsertIn(ApiSchema):
    category_id: str
    name: str = Field(min_length=1, max_length=120)
    years_of_experience: int | None = Field(default=None, ge=0)
    icon_key: str | None = Field(default=None, max_length=80)
    sort_order: int = 0
    is_highlighted: bool = False


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


class AdminBlogTagOut(ApiSchema):
    id: str
    name: str
    slug: str


class AdminBlogTagUpsertIn(ApiSchema):
    name: str = Field(min_length=1, max_length=120)
    slug: str | None = Field(default=None, max_length=120)


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


class AdminNavigationItemUpsertIn(ApiSchema):
    label: str = Field(min_length=1, max_length=120)
    route_path: str = Field(min_length=1, max_length=255)
    is_external: bool = False
    sort_order: int = 0
    is_visible: bool = True


class AdminNavigationItemOut(ApiSchema):
    id: str
    label: str
    route_path: str
    is_external: bool
    sort_order: int
    is_visible: bool


class AdminNavigationItemsListOut(ApiSchema):
    items: list[AdminNavigationItemOut]
    total: int


class AdminGithubContributionDayIn(ApiSchema):
    date: str
    count: int = Field(ge=0)
    level: int = Field(ge=0)


class AdminGithubContributionDayOut(ApiSchema):
    date: str
    count: int
    level: int


class AdminGithubSnapshotUpsertIn(ApiSchema):
    snapshot_date: str
    username: str = Field(min_length=1, max_length=120)
    public_repo_count: int = Field(ge=0)
    followers_count: int | None = Field(default=None, ge=0)
    following_count: int | None = Field(default=None, ge=0)
    total_stars: int | None = Field(default=None, ge=0)
    total_commits: int | None = Field(default=None, ge=0)
    raw_payload: dict[str, Any] | None = None
    contribution_days: list[AdminGithubContributionDayIn] = Field(default_factory=list)


class AdminGithubSnapshotOut(ApiSchema):
    id: str
    snapshot_date: str
    username: str
    public_repo_count: int
    followers_count: int | None = None
    following_count: int | None = None
    total_stars: int | None = None
    total_commits: int | None = None
    raw_payload: dict[str, Any] | None = None
    contribution_days: list[AdminGithubContributionDayOut]
    created_at: str
    updated_at: str


class AdminGithubSnapshotsListOut(ApiSchema):
    items: list[AdminGithubSnapshotOut]
    total: int


class AdminGithubSnapshotRefreshIn(ApiSchema):
    username: str | None = Field(default=None, max_length=120)
    prune_history: bool = True


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


class AdminSiteEventOut(ApiSchema):
    id: str
    event_type: str
    page_path: str
    visitor_id: str
    session_id: str | None = None
    referrer: str | None = None
    user_agent: str | None = None
    ip_address: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: str


class AdminVisitSessionSummaryOut(ApiSchema):
    session_id: str
    visitor_id: str
    started_at: str
    last_activity_at: str
    total_events: int
    page_views: int
    assistant_messages: int
    contact_submissions: int
    entry_page_path: str | None = None
    last_page_path: str | None = None
    ip_address: str | None = None


class AdminVisitorActivitySummaryOut(ApiSchema):
    visitor_id: str
    first_seen_at: str
    last_seen_at: str
    total_events: int
    unique_sessions: int
    page_views: int
    assistant_messages: int
    contact_submissions: int
    latest_page_path: str | None = None
    latest_ip_address: str | None = None


class AdminAssistantConversationSummaryOut(ApiSchema):
    id: str
    session_id: str
    visitor_id: str | None = None
    site_session_id: str | None = None
    page_path: str | None = None
    started_at: str
    last_message_at: str
    total_messages: int
    user_message_count: int
    assistant_message_count: int
    used_fallback: bool | None = None
    first_user_message: str | None = None
    latest_assistant_message: str | None = None


class AdminSiteActivitySummaryOut(ApiSchema):
    total_events: int
    unique_visitors: int
    page_views: int
    assistant_messages: int
    contact_submissions: int


class AdminSiteActivityOut(ApiSchema):
    summary: AdminSiteActivitySummaryOut
    visitors: list[AdminVisitorActivitySummaryOut]
    visits: list[AdminVisitSessionSummaryOut]
    events: list[AdminSiteEventOut]
    assistant_conversations: list[AdminAssistantConversationSummaryOut]


class AdminAssistantKnowledgeStatusOut(ApiSchema):
    total_documents: int
    total_chunks: int
    documents_by_source_type: dict[str, int]
    latest_updated_at: str | None = None


class AdminAssistantKnowledgeRebuildIn(ApiSchema):
    pass


class AdminAssistantKnowledgeRebuildOut(AdminAssistantKnowledgeStatusOut):
    pass

class AdminReferenceDataOut(ApiSchema):
    skills: list[AdminSkillOut]
    skill_categories: list[AdminSkillCategoryOut]
    media_files: list[AdminMediaFileOut]
    blog_tags: list[AdminBlogTagOut]
    project_states: list[ProjectStateLiteral]
    publication_statuses: list[PublicationStatusLiteral]


class AdminDashboardSummaryOut(ApiSchema):
    projects: int
    blog_posts: int
    unread_messages: int
    skills: int
    skill_categories: int
    media_files: int
    experiences: int
    navigation_items: int
    blog_tags: int
    admin_users: int
    github_snapshots: int
