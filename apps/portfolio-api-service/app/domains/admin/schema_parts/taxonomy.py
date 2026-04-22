from __future__ import annotations

from pydantic import Field

from app.schemas.base import ApiSchema


class AdminSkillCategoryOut(ApiSchema):
    id: str
    name: str
    name_nl: str | None = None
    description: str | None = None
    description_nl: str | None = None
    icon_key: str | None = None
    sort_order: int


class AdminSkillCategoryUpsertIn(ApiSchema):
    name: str = Field(min_length=1, max_length=120)
    name_nl: str | None = Field(default=None, max_length=120)
    description: str | None = None
    description_nl: str | None = None
    icon_key: str | None = Field(default=None, max_length=80)
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
    years_of_experience: int | None = Field(default=None, ge=0, le=80)
    icon_key: str | None = Field(default=None, max_length=80)
    sort_order: int = 0
    is_highlighted: bool = False


class AdminBlogTagOut(ApiSchema):
    id: str
    name: str
    slug: str


class AdminBlogTagUpsertIn(ApiSchema):
    name: str = Field(min_length=1, max_length=120)
    slug: str | None = Field(default=None, max_length=120)


__all__ = [
    'AdminBlogTagOut',
    'AdminBlogTagUpsertIn',
    'AdminSkillCategoryOut',
    'AdminSkillCategoryUpsertIn',
    'AdminSkillOut',
    'AdminSkillUpsertIn',
]
