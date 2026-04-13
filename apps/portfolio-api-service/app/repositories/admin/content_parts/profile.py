from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Profile, SocialLink
from app.schemas.admin import AdminProfileOut, AdminProfileUpdateIn


class AdminProfileContentRepository:
    def get_profile(self) -> AdminProfileOut | None:
        profile = self.session.scalar(
            select(Profile)
            .options(
                selectinload(Profile.avatar_file),
                selectinload(Profile.hero_image_file),
                selectinload(Profile.resume_file),
                selectinload(Profile.social_links),
            )
            .order_by(Profile.updated_at.desc())
        )
        return self._map_profile(profile) if profile else None

    def update_profile(self, payload: AdminProfileUpdateIn) -> AdminProfileOut | None:
        profile = self.session.scalar(
            select(Profile)
            .options(selectinload(Profile.social_links))
            .order_by(Profile.updated_at.desc())
        )
        if profile is None:
            return None

        profile.first_name = payload.first_name
        profile.last_name = payload.last_name
        profile.headline = payload.headline
        profile.short_intro = payload.short_intro
        profile.long_bio = self._normalize_optional_text(payload.long_bio)
        profile.location = self._normalize_optional_text(payload.location)
        profile.email = str(payload.email).strip() if payload.email else None
        profile.phone = self._normalize_optional_text(payload.phone)
        profile.avatar_file_id = self._optional_uuid(payload.avatar_file_id)
        profile.hero_image_file_id = self._optional_uuid(payload.hero_image_file_id)
        profile.resume_file_id = self._optional_uuid(payload.resume_file_id)
        profile.cta_primary_label = self._normalize_optional_text(payload.cta_primary_label)
        profile.cta_primary_url = self._normalize_optional_text(payload.cta_primary_url)
        profile.cta_secondary_label = self._normalize_optional_text(payload.cta_secondary_label)
        profile.cta_secondary_url = self._normalize_optional_text(payload.cta_secondary_url)
        profile.is_public = payload.is_public

        profile.social_links.clear()
        for index, link in enumerate(payload.social_links):
            profile.social_links.append(
                SocialLink(
                    id=self._optional_uuid(link.id),
                    platform=link.platform.lower(),
                    label=link.label,
                    url=link.url,
                    icon_key=self._normalize_optional_text(link.icon_key),
                    sort_order=link.sort_order if link.sort_order is not None else index,
                    is_visible=link.is_visible,
                )
            )

        self.session.commit()
        return self.get_profile()
