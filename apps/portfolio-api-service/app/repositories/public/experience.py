from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Experience, ExperienceSkill
from app.schemas.public import ExperienceOut


class PublicExperienceRepositoryMixin:
    def list_experience(self) -> list[ExperienceOut]:
        items = self.session.scalars(
            select(Experience)
            .options(
                selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill),
                selectinload(Experience.logo_file),
            )
            .order_by(Experience.sort_order.asc(), Experience.start_date.desc())
        ).all()
        return [self._map_experience(item) for item in items]

    def _list_experience_preview(self, limit: int) -> list[ExperienceOut]:
        items = self.session.scalars(
            select(Experience)
            .options(
                selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill),
                selectinload(Experience.logo_file),
            )
            .order_by(Experience.sort_order.asc(), Experience.start_date.desc())
            .limit(limit)
        ).all()
        return [self._map_experience(item) for item in items]

    def _map_experience(self, item: Experience) -> ExperienceOut:
        ordered_skills = sorted([link.skill.name for link in item.skill_links if link.skill is not None])
        return ExperienceOut(
            id=str(item.id),
            organization_name=item.organization_name,
            role_title=item.role_title,
            location=item.location,
            experience_type=item.experience_type,
            start_date=item.start_date.isoformat(),
            end_date=item.end_date.isoformat() if item.end_date else None,
            is_current=item.is_current,
            summary=item.summary,
            description_markdown=item.description_markdown,
            logo_file_id=str(item.logo_file_id) if item.logo_file_id else None,
            logo=self._map_media(item.logo_file, alt=item.organization_name),
            sort_order=item.sort_order,
            skill_names=ordered_skills,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat(),
        )
