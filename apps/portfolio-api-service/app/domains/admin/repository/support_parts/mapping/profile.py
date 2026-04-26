from __future__ import annotations

from app.db.models import Profile, Skill, SkillCategory
from app.domains.admin.schema import AdminProfileOut, AdminSkillCategoryOut, AdminSkillOut, AdminSocialLinkOut


class AdminRepositoryProfileMappingMixin:
    def _map_profile(self, profile: Profile) -> AdminProfileOut:
        return AdminProfileOut(
            id=str(profile.id),
            first_name=profile.first_name,
            last_name=profile.last_name,
            headline=profile.headline,
            headline_nl=profile.headline_nl,
            short_intro=profile.short_intro,
            short_intro_nl=profile.short_intro_nl,
            long_bio=profile.long_bio,
            long_bio_nl=profile.long_bio_nl,
            location=profile.location,
            email=profile.email,
            phone=profile.phone,
            avatar_file_id=str(profile.avatar_file_id) if profile.avatar_file_id else None,
            hero_image_file_id=str(profile.hero_image_file_id) if profile.hero_image_file_id else None,
            resume_file_id=str(profile.resume_file_id) if profile.resume_file_id else None,
            resume_file_id_nl=str(profile.resume_file_id_nl) if profile.resume_file_id_nl else None,
            avatar=self._map_media(profile.avatar_file, alt=f'{profile.first_name} {profile.last_name} avatar'),
            hero_image=self._map_media(profile.hero_image_file, alt=f'{profile.first_name} {profile.last_name} hero image'),
            resume=self._map_media(profile.resume_file, alt=f'{profile.first_name} {profile.last_name} resume'),
            resume_nl=self._map_media(profile.resume_file_nl, alt=f'{profile.first_name} {profile.last_name} Dutch resume'),
            cta_primary_label=profile.cta_primary_label,
            cta_primary_label_nl=profile.cta_primary_label_nl,
            cta_primary_url=profile.cta_primary_url,
            cta_secondary_label=profile.cta_secondary_label,
            cta_secondary_label_nl=profile.cta_secondary_label_nl,
            cta_secondary_url=profile.cta_secondary_url,
            is_public=profile.is_public,
            social_links=[
                AdminSocialLinkOut(
                    id=str(link.id),
                    platform=link.platform,
                    label=link.label,
                    url=link.url,
                    icon_key=link.icon_key,
                    sort_order=link.sort_order,
                    is_visible=link.is_visible,
                )
                for link in sorted(profile.social_links, key=lambda item: (item.sort_order, item.label.lower()))
            ],
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat(),
        )

    def _map_skill_category(self, category: SkillCategory) -> AdminSkillCategoryOut:
        return AdminSkillCategoryOut(
            id=str(category.id),
            name=category.name,
            name_nl=category.name_nl,
            description=category.description,
            description_nl=category.description_nl,
            icon_key=category.icon_key,
            sort_order=category.sort_order,
        )

    def _map_admin_skill(self, skill: Skill) -> AdminSkillOut:
        return AdminSkillOut(
            id=str(skill.id),
            category_id=str(skill.category_id),
            name=skill.name,
            years_of_experience=skill.years_of_experience,
            proficiency_label=skill.proficiency_label,
            proficiency_label_nl=skill.proficiency_label_nl,
            icon_key=skill.icon_key,
            sort_order=skill.sort_order,
            is_highlighted=skill.is_highlighted,
        )
