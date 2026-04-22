from __future__ import annotations

from app.db.models import Experience
from app.domains.admin.schema import AdminExperienceOut


class AdminRepositoryExperienceMappingMixin:
    def _map_experience(self, experience: Experience) -> AdminExperienceOut:
        ordered_skills = sorted(experience.skill_links, key=lambda link: (link.skill.sort_order, link.skill.name.lower()))

        return AdminExperienceOut(
            id=str(experience.id),
            organization_name=experience.organization_name,
            role_title=experience.role_title,
            role_title_nl=experience.role_title_nl,
            location=experience.location,
            experience_type=experience.experience_type,
            start_date=experience.start_date.isoformat(),
            end_date=experience.end_date.isoformat() if experience.end_date else None,
            is_current=experience.is_current,
            summary=experience.summary,
            summary_nl=experience.summary_nl,
            description_markdown=experience.description_markdown,
            description_markdown_nl=experience.description_markdown_nl,
            logo_file_id=str(experience.logo_file_id) if experience.logo_file_id else None,
            logo=self._map_media(experience.logo_file, alt=f'{experience.organization_name} logo'),
            sort_order=experience.sort_order,
            created_at=experience.created_at.isoformat(),
            updated_at=experience.updated_at.isoformat(),
            skill_ids=[str(link.skill_id) for link in ordered_skills],
            skills=[self._map_skill(link.skill) for link in ordered_skills],
        )
