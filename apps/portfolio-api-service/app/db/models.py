from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.types import Vector


class EventType(str, Enum):
    PAGE_VIEW = 'page_view'
    PORTFOLIO_LIKE = 'portfolio_like'
    BLOG_VIEW = 'blog_view'
    PROJECT_CLICK = 'project_click'
    CONTACT_SUBMIT = 'contact_submit'
    ASSISTANT_MESSAGE = 'assistant_message'


class AssistantRole(str, Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class KnowledgeSourceType(str, Enum):
    PROFILE = 'profile'
    PROJECT = 'project'
    BLOG_POST = 'blog_post'
    EXPERIENCE = 'experience'


class MediaVisibility(str, Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'
    SIGNED = 'signed'


class ProjectState(str, Enum):
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    COMPLETED = 'completed'
    PAUSED = 'paused'


class PublicationStatus(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'


class NavigationItem(Base):
    __tablename__ = 'navigation_items'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    route_path: Mapped[str] = mapped_column(String(255), nullable=False)
    is_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class AdminUser(TimestampMixin, Base):
    __tablename__ = 'admin_users'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    uploaded_media_files: Mapped[list['MediaFile']] = relationship(back_populates='uploaded_by')


class SiteEvent(Base):
    __tablename__ = 'site_events'
    __table_args__ = (
        Index('ix_site_events_event_type_created_at', 'event_type', 'created_at'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    session_id: Mapped[str | None] = mapped_column(String(255))
    visitor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    page_path: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[EventType] = mapped_column(SqlEnum(EventType, native_enum=False), nullable=False)
    referrer: Mapped[str | None] = mapped_column(String(500))
    user_agent: Mapped[str | None] = mapped_column(String(500))
    metadata_json: Mapped[dict | None] = mapped_column('metadata', JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class GithubSnapshot(Base):
    __tablename__ = 'github_snapshots'
    __table_args__ = (
        UniqueConstraint('snapshot_date', 'username', name='uq_github_snapshots_date_username'),
        CheckConstraint('public_repo_count >= 0', name='ck_github_snapshots_public_repo_count_nonnegative'),
        CheckConstraint('followers_count IS NULL OR followers_count >= 0', name='ck_github_snapshots_followers_nonnegative'),
        CheckConstraint('following_count IS NULL OR following_count >= 0', name='ck_github_snapshots_following_nonnegative'),
        CheckConstraint('total_stars IS NULL OR total_stars >= 0', name='ck_github_snapshots_total_stars_nonnegative'),
        CheckConstraint('total_commits IS NULL OR total_commits >= 0', name='ck_github_snapshots_total_commits_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    public_repo_count: Mapped[int] = mapped_column(Integer, nullable=False)
    followers_count: Mapped[int | None] = mapped_column(Integer)
    following_count: Mapped[int | None] = mapped_column(Integer)
    total_stars: Mapped[int | None] = mapped_column(Integer)
    total_commits: Mapped[int | None] = mapped_column(Integer)
    raw_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    contribution_days: Mapped[list['GithubContributionDay']] = relationship(
        back_populates='snapshot', cascade='all, delete-orphan'
    )


class GithubContributionDay(Base):
    __tablename__ = 'github_contribution_days'
    __table_args__ = (
        UniqueConstraint('snapshot_id', 'contribution_date', name='uq_github_contribution_days_snapshot_date'),
        CheckConstraint('contribution_count >= 0', name='ck_github_contribution_days_count_nonnegative'),
        CheckConstraint('level >= 0', name='ck_github_contribution_days_level_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    snapshot_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('github_snapshots.id', ondelete='CASCADE'), nullable=False
    )
    contribution_date: Mapped[date] = mapped_column(Date, nullable=False)
    contribution_count: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    snapshot: Mapped[GithubSnapshot] = relationship(back_populates='contribution_days')


class ContactMessage(TimestampMixin, Base):
    __tablename__ = 'contact_messages'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    subject: Mapped[str] = mapped_column(String(120), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    source_page: Mapped[str] = mapped_column(String(255), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AssistantConversation(Base):
    __tablename__ = 'assistant_conversations'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    session_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_message_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    messages: Mapped[list['AssistantMessage']] = relationship(
        back_populates='conversation', cascade='all, delete-orphan'
    )


class AssistantMessage(Base):
    __tablename__ = 'assistant_messages'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    conversation_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('assistant_conversations.id', ondelete='CASCADE'), nullable=False
    )
    role: Mapped[AssistantRole] = mapped_column(SqlEnum(AssistantRole, native_enum=False), nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    conversation: Mapped[AssistantConversation] = relationship(back_populates='messages')


class KnowledgeDocument(TimestampMixin, Base):
    __tablename__ = 'knowledge_documents'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    source_type: Mapped[KnowledgeSourceType] = mapped_column(
        SqlEnum(KnowledgeSourceType, native_enum=False), nullable=False
    )
    source_id: Mapped[UUID | None] = mapped_column(Uuid)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    canonical_url: Mapped[str | None] = mapped_column(String(500))
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    content_platform: Mapped[str | None] = mapped_column(String(120))
    metadata_json: Mapped[dict] = mapped_column('metadata', JSON, nullable=False, default=dict)

    chunks: Mapped[list['KnowledgeChunk']] = relationship(
        back_populates='document', cascade='all, delete-orphan'
    )


class KnowledgeChunk(Base):
    __tablename__ = 'knowledge_chunks'
    __table_args__ = (
        UniqueConstraint('document_id', 'chunk_index', name='uq_knowledge_chunks_document_chunk_index'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    document_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('knowledge_documents.id', ondelete='CASCADE'), nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_vector: Mapped[str | None] = mapped_column(Vector())
    metadata_json: Mapped[dict | None] = mapped_column('metadata', JSON)

    document: Mapped[KnowledgeDocument] = relationship(back_populates='chunks')


class MediaFile(TimestampMixin, Base):
    __tablename__ = 'media_files'
    __table_args__ = (
        UniqueConstraint('object_key', name='uq_media_files_object_key'),
        CheckConstraint('file_size_bytes IS NULL OR file_size_bytes >= 0', name='ck_media_files_file_size_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    bucket_name: Mapped[str] = mapped_column(String(120), nullable=False)
    object_key: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str | None] = mapped_column(String(255))
    mime_type: Mapped[str | None] = mapped_column(String(120))
    file_size_bytes: Mapped[int | None] = mapped_column(Integer)
    checksum: Mapped[str | None] = mapped_column(String(255))
    public_url: Mapped[str | None] = mapped_column(String(500))
    alt_text: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    visibility: Mapped[MediaVisibility] = mapped_column(
        SqlEnum(MediaVisibility, native_enum=False), nullable=False
    )
    uploaded_by_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('admin_users.id', ondelete='SET NULL'))

    uploaded_by: Mapped['AdminUser | None'] = relationship(back_populates='uploaded_media_files')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    profile_avatar_for: Mapped[list['Profile']] = relationship(
        'Profile',
        foreign_keys=lambda: [Profile.avatar_file_id],
        back_populates='avatar_file',
    )
    profile_hero_for: Mapped[list['Profile']] = relationship(
        'Profile',
        foreign_keys=lambda: [Profile.hero_image_file_id],
        back_populates='hero_image_file',
    )
    profile_resume_for: Mapped[list['Profile']] = relationship(
        'Profile',
        foreign_keys=lambda: [Profile.resume_file_id],
        back_populates='resume_file',
    )
    experience_logo_for: Mapped[list['Experience']] = relationship(
        'Experience',
        foreign_keys=lambda: [Experience.logo_file_id],
        back_populates='logo_file',
    )
    project_cover_for: Mapped[list['Project']] = relationship(
        'Project',
        foreign_keys=lambda: [Project.cover_image_file_id],
        back_populates='cover_image_file',
    )
    project_images: Mapped[list['ProjectImage']] = relationship(
        'ProjectImage',
        foreign_keys=lambda: [ProjectImage.image_file_id],
        back_populates='image_file',
    )
    blog_cover_for: Mapped[list['BlogPost']] = relationship(
        'BlogPost',
        foreign_keys=lambda: [BlogPost.cover_image_file_id],
        back_populates='cover_image_file',
    )


class Profile(TimestampMixin, Base):
    __tablename__ = 'profiles'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    headline: Mapped[str] = mapped_column(String(255), nullable=False)
    short_intro: Mapped[str] = mapped_column(Text, nullable=False)
    long_bio: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(320))
    phone: Mapped[str | None] = mapped_column(String(64))
    avatar_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    hero_image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    resume_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    cta_primary_label: Mapped[str | None] = mapped_column(String(120))
    cta_primary_url: Mapped[str | None] = mapped_column(String(500))
    cta_secondary_label: Mapped[str | None] = mapped_column(String(120))
    cta_secondary_url: Mapped[str | None] = mapped_column(String(500))
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    avatar_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys=lambda: [Profile.avatar_file_id],
        back_populates='profile_avatar_for',
    )
    hero_image_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys=lambda: [Profile.hero_image_file_id],
        back_populates='profile_hero_for',
    )
    resume_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys=lambda: [Profile.resume_file_id],
        back_populates='profile_resume_for',
    )
    social_links: Mapped[list['SocialLink']] = relationship(
        back_populates='profile', cascade='all, delete-orphan', order_by='SocialLink.sort_order'
    )


class SocialLink(Base):
    __tablename__ = 'social_links'
    __table_args__ = (
        UniqueConstraint('profile_id', 'platform', name='uq_social_links_profile_platform'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    profile_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    icon_key: Mapped[str | None] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    profile: Mapped[Profile] = relationship(back_populates='social_links')


class SkillCategory(Base):
    __tablename__ = 'skill_categories'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    skills: Mapped[list['Skill']] = relationship(back_populates='category')


class Skill(Base):
    __tablename__ = 'skills'
    __table_args__ = (
        CheckConstraint('years_of_experience IS NULL OR years_of_experience >= 0', name='ck_skills_years_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    category_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('skill_categories.id', ondelete='RESTRICT'), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    years_of_experience: Mapped[int | None] = mapped_column(Integer)
    icon_key: Mapped[str | None] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_highlighted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    category: Mapped[SkillCategory] = relationship(back_populates='skills')
    project_links: Mapped[list['ProjectSkill']] = relationship(back_populates='skill', cascade='all, delete-orphan')
    experience_links: Mapped[list['ExperienceSkill']] = relationship(back_populates='skill', cascade='all, delete-orphan')


class Experience(TimestampMixin, Base):
    __tablename__ = 'experience'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255))
    experience_type: Mapped[str] = mapped_column(String(80), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    description_markdown: Mapped[str | None] = mapped_column(Text)
    logo_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    logo_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys=lambda: [Experience.logo_file_id],
        back_populates='experience_logo_for',
    )
    skill_links: Mapped[list['ExperienceSkill']] = relationship(
        back_populates='experience', cascade='all, delete-orphan'
    )


class ExperienceSkill(Base):
    __tablename__ = 'experience_skills'

    experience_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('experience.id', ondelete='CASCADE'), primary_key=True
    )
    skill_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True
    )

    experience: Mapped[Experience] = relationship(back_populates='skill_links')
    skill: Mapped[Skill] = relationship(back_populates='experience_links')


class Project(TimestampMixin, Base):
    __tablename__ = 'projects'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    teaser: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    description_markdown: Mapped[str | None] = mapped_column(Text)
    cover_image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    github_url: Mapped[str | None] = mapped_column(String(500))
    github_repo_owner: Mapped[str | None] = mapped_column(String(120))
    github_repo_name: Mapped[str | None] = mapped_column(String(120))
    demo_url: Mapped[str | None] = mapped_column(String(500))
    company_name: Mapped[str | None] = mapped_column(String(255))
    started_on: Mapped[date | None] = mapped_column(Date)
    ended_on: Mapped[date | None] = mapped_column(Date)
    duration_label: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[ProjectState] = mapped_column(SqlEnum(ProjectState, native_enum=False), nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    cover_image_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys=lambda: [Project.cover_image_file_id],
        back_populates='project_cover_for',
    )
    skill_links: Mapped[list['ProjectSkill']] = relationship(back_populates='project', cascade='all, delete-orphan')
    images: Mapped[list['ProjectImage']] = relationship(
        back_populates='project', cascade='all, delete-orphan', order_by='ProjectImage.sort_order'
    )


class ProjectSkill(Base):
    __tablename__ = 'project_skills'

    project_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('projects.id', ondelete='CASCADE'), primary_key=True
    )
    skill_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True
    )

    project: Mapped[Project] = relationship(back_populates='skill_links')
    skill: Mapped[Skill] = relationship(back_populates='project_links')


class ProjectImage(Base):
    __tablename__ = 'project_images'
    __table_args__ = (
        UniqueConstraint('project_id', 'image_file_id', name='uq_project_images_project_file'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    project_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    alt_text: Mapped[str | None] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_cover: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    project: Mapped[Project] = relationship(back_populates='images')
    image_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys=lambda: [ProjectImage.image_file_id],
        back_populates='project_images',
    )


class BlogPost(TimestampMixin, Base):
    __tablename__ = 'blog_posts'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    cover_image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    cover_image_alt: Mapped[str | None] = mapped_column(String(255))
    reading_time_minutes: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[PublicationStatus] = mapped_column(
        SqlEnum(PublicationStatus, native_enum=False), nullable=False
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    seo_title: Mapped[str | None] = mapped_column(String(255))
    seo_description: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    cover_image_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys=lambda: [BlogPost.cover_image_file_id],
        back_populates='blog_cover_for',
    )
    tag_links: Mapped[list['BlogPostTag']] = relationship(back_populates='post', cascade='all, delete-orphan')


class BlogTag(Base):
    __tablename__ = 'blog_tags'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

    post_links: Mapped[list['BlogPostTag']] = relationship(back_populates='tag', cascade='all, delete-orphan')


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
