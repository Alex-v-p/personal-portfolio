from __future__ import annotations

from app.db.models import MediaFile, Skill
from app.domains.public_site.schema import PublicMediaAssetOut, SkillSummaryOut


class AdminRepositoryMappingCommonMixin:
    def _map_skill(self, skill: Skill) -> SkillSummaryOut:
        return SkillSummaryOut(
            id=str(skill.id),
            category_id=str(skill.category_id),
            name=skill.name,
            years_of_experience=skill.years_of_experience,
            proficiency_label=skill.proficiency_label,
            display_label=skill.proficiency_label or (f'{skill.years_of_experience}y' if skill.years_of_experience is not None else None),
            icon_key=skill.icon_key,
            sort_order=skill.sort_order,
            is_highlighted=skill.is_highlighted,
        )

    def _media_folder(self, media_file: MediaFile) -> str | None:
        object_key = (media_file.object_key or '').strip('/')
        if not object_key or '/' not in object_key:
            return None
        folder = object_key.rsplit('/', 1)[0].strip('/')
        return folder or None

    def _map_media(self, media_file: MediaFile | None, alt: str | None = None) -> PublicMediaAssetOut | None:
        url = self.media_resolver.resolve(media_file)

        if media_file is None or url is None:
            return None

        return PublicMediaAssetOut(
            id=str(media_file.id),
            url=url,
            alt=media_file.alt_text or alt,
            file_name=media_file.original_filename,
            mime_type=media_file.mime_type,
            width=None,
            height=None,
        )
