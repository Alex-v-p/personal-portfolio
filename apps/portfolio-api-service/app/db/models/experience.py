from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.media import MediaFile
    from app.db.models.taxonomy import Skill


class Experience(TimestampMixin, Base):
    __tablename__ = 'experience'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255))
    experience_type: Mapped[str] = mapped_column(String(80), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    description_markdown: Mapped[str | None] = mapped_column(Text)
    logo_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    logo_file: Mapped[MediaFile | None] = relationship(
        'MediaFile',
        foreign_keys='Experience.logo_file_id',
        back_populates='experience_logo_for',
    )
    skill_links: Mapped[list[ExperienceSkill]] = relationship(
        back_populates='experience', cascade='all, delete-orphan'
    )


class ExperienceSkill(Base):
    __tablename__ = 'experience_skills'

    experience_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('experience.id', ondelete='CASCADE'), primary_key=True
    )
    skill_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True
    )

    experience: Mapped[Experience] = relationship(back_populates='skill_links')
    skill: Mapped[Skill] = relationship(back_populates='experience_links')
