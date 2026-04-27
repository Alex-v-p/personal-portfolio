from __future__ import annotations

from pydantic import Field

from app.domains.admin.schema_parts.common import ProjectStateLiteral
from app.schemas.base import ApiSchema
from app.domains.public_site.schema import PublicMediaAssetOut, SkillSummaryOut


class AdminProjectImageIn(ApiSchema):
    image_file_id: str | None = None
    alt_text: str | None = Field(default=None, max_length=255)
    alt_text_nl: str | None = Field(default=None, max_length=255)
    sort_order: int = 0
    is_cover: bool = False


class AdminProjectImageOut(ApiSchema):
    id: str
    project_id: str
    image_file_id: str | None = None
    alt_text: str | None = None
    alt_text_nl: str | None = None
    sort_order: int
    is_cover: bool
    image: PublicMediaAssetOut | None = None


class AdminProjectUpsertIn(ApiSchema):
    slug: str | None = Field(default=None, max_length=160)
    title: str = Field(min_length=1, max_length=255)
    title_nl: str | None = Field(default=None, max_length=255)
    teaser: str = Field(min_length=1)
    teaser_nl: str | None = None
    summary: str | None = None
    summary_nl: str | None = None
    description_markdown: str | None = None
    description_markdown_nl: str | None = None
    cover_image_file_id: str | None = None
    github_url: str | None = Field(default=None, max_length=500)
    github_repo_owner: str | None = Field(default=None, max_length=120)
    github_repo_name: str | None = Field(default=None, max_length=120)
    demo_url: str | None = Field(default=None, max_length=500)
    company_name: str | None = Field(default=None, max_length=255)
    started_on: str | None = None
    ended_on: str | None = None
    duration_label: str = Field(min_length=1, max_length=120)
    duration_label_nl: str | None = Field(default=None, max_length=120)
    status: str = Field(min_length=1, max_length=120)
    status_nl: str | None = Field(default=None, max_length=120)
    state: ProjectStateLiteral
    is_featured: bool = False
    sort_order: int = 0
    published_at: str | None = None
    skill_ids: list[str] = Field(default_factory=list)
    images: list[AdminProjectImageIn] = Field(default_factory=list)


class AdminProjectOut(ApiSchema):
    id: str
    slug: str
    title: str
    title_nl: str | None = None
    teaser: str
    teaser_nl: str | None = None
    summary: str | None = None
    summary_nl: str | None = None
    description_markdown: str | None = None
    description_markdown_nl: str | None = None
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
    duration_label_nl: str | None = None
    status: str
    status_nl: str | None = None
    state: ProjectStateLiteral
    is_featured: bool
    sort_order: int
    published_at: str
    created_at: str
    updated_at: str
    skill_ids: list[str]
    skills: list[SkillSummaryOut]
    images: list[AdminProjectImageOut]


class AdminProjectsListOut(ApiSchema):
    items: list[AdminProjectOut]
    total: int


__all__ = ['AdminProjectImageIn', 'AdminProjectImageOut', 'AdminProjectOut', 'AdminProjectUpsertIn', 'AdminProjectsListOut']
