from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.experience import ExperienceSkill
    from app.db.models.projects import ProjectSkill


class SkillCategory(Base):
    __tablename__ = 'skill_categories'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    name_nl: Mapped[str | None] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    description_nl: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    skills: Mapped[list[Skill]] = relationship(back_populates='category')


class Skill(Base):
    __tablename__ = 'skills'
    __table_args__ = (
        CheckConstraint('years_of_experience IS NULL OR years_of_experience >= 0', name='ck_skills_years_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    category_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('skill_categories.id', ondelete='RESTRICT'), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    years_of_experience: Mapped[int | None] = mapped_column(Integer)
    icon_key: Mapped[str | None] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_highlighted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    category: Mapped[SkillCategory] = relationship(back_populates='skills')
    project_links: Mapped[list[ProjectSkill]] = relationship(back_populates='skill', cascade='all, delete-orphan')
    experience_links: Mapped[list[ExperienceSkill]] = relationship(back_populates='skill', cascade='all, delete-orphan')
