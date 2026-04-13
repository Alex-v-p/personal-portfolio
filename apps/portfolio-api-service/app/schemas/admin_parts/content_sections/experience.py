from __future__ import annotations

from pydantic import Field

from app.schemas.base import ApiSchema
from app.schemas.public import PublicMediaAssetOut, SkillSummaryOut


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


__all__ = ['AdminExperienceOut', 'AdminExperienceUpsertIn', 'AdminExperiencesListOut']
