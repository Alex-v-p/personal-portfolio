from __future__ import annotations

from app.schemas.base import ApiSchema

from .common import PublicMediaAssetOut


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


class ExpertiseSkillOut(ApiSchema):
    name: str
    years_of_experience: int | None = None


class ExpertiseGroupOut(ApiSchema):
    title: str
    tags: list[str]
    skills: list[ExpertiseSkillOut] = []


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


class SiteShellOut(ApiSchema):
    navigation: NavigationListOut
    profile: ProfileOut
    footer_text: str
    contact_methods: list[ContactMethodOut]


__all__ = [
    'ContactMethodOut',
    'ExpertiseGroupOut',
    'ExpertiseSkillOut',
    'NavigationItemOut',
    'NavigationListOut',
    'ProfileOut',
    'SiteShellOut',
    'SocialLinkOut',
]
