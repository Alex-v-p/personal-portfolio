from __future__ import annotations

from app.schemas.base import ApiSchema

from .common import PublicMediaAssetOut


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


__all__ = ['ExperienceListOut', 'ExperienceOut']
