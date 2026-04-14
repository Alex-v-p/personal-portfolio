from __future__ import annotations

from pydantic import EmailStr, Field

from app.schemas.base import ApiSchema
from app.domains.public_site.schema import PublicMediaAssetOut


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
    social_links: list['AdminSocialLinkIn'] = Field(default_factory=list)


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


__all__ = [
    'AdminProfileOut',
    'AdminProfileUpdateIn',
    'AdminSocialLinkIn',
    'AdminSocialLinkOut',
]
