from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Experience, ExperienceSkill
from app.domains.admin.schema import AdminExperienceOut, AdminExperienceUpsertIn


class AdminExperienceContentRepository:
    def list_experiences(self) -> list[AdminExperienceOut]:
        experiences = self.session.scalars(
            select(Experience)
            .options(
                selectinload(Experience.logo_file),
                selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill),
            )
            .order_by(Experience.sort_order.asc(), Experience.start_date.desc(), Experience.organization_name.asc())
        ).all()
        return [self._map_experience(experience) for experience in experiences]

    def get_experience(self, experience_id: UUID) -> AdminExperienceOut | None:
        experience = self.session.scalar(
            select(Experience)
            .options(
                selectinload(Experience.logo_file),
                selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill),
            )
            .where(Experience.id == experience_id)
        )
        return self._map_experience(experience) if experience else None

    def create_experience(self, payload: AdminExperienceUpsertIn) -> AdminExperienceOut:
        experience = Experience(
            organization_name=payload.organization_name,
            role_title=payload.role_title,
            location=self._normalize_optional_text(payload.location),
            experience_type=payload.experience_type,
            start_date=self._parse_date(payload.start_date) or date.today(),
            end_date=self._parse_date(payload.end_date),
            is_current=payload.is_current,
            summary=payload.summary,
            description_markdown=self._normalize_optional_text(payload.description_markdown),
            logo_file_id=self._optional_uuid(payload.logo_file_id),
            sort_order=payload.sort_order,
        )
        self.session.add(experience)
        self.session.flush()
        self._replace_experience_skill_links(experience, payload.skill_ids)
        self.session.commit()
        return self.get_experience(experience.id)  # type: ignore[return-value]

    def update_experience(self, experience_id: UUID, payload: AdminExperienceUpsertIn) -> AdminExperienceOut | None:
        experience = self.session.get(Experience, experience_id)
        if experience is None:
            return None
        experience.organization_name = payload.organization_name
        experience.role_title = payload.role_title
        experience.location = self._normalize_optional_text(payload.location)
        experience.experience_type = payload.experience_type
        experience.start_date = self._parse_date(payload.start_date) or experience.start_date
        experience.end_date = self._parse_date(payload.end_date)
        experience.is_current = payload.is_current
        experience.summary = payload.summary
        experience.description_markdown = self._normalize_optional_text(payload.description_markdown)
        experience.logo_file_id = self._optional_uuid(payload.logo_file_id)
        experience.sort_order = payload.sort_order
        self._replace_experience_skill_links(experience, payload.skill_ids)
        self.session.commit()
        return self.get_experience(experience_id)

    def delete_experience(self, experience_id: UUID) -> bool:
        experience = self.session.get(Experience, experience_id)
        if experience is None:
            return False
        self.session.delete(experience)
        self.session.commit()
        return True
