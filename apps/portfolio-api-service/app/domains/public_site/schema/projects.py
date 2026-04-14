from __future__ import annotations

from typing import Literal

from app.schemas.base import ApiSchema

from .common import PublicMediaAssetOut


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


__all__ = [
    'ProjectDetailOut',
    'ProjectImageOut',
    'ProjectsListOut',
    'ProjectSummaryOut',
    'SkillSummaryOut',
]
