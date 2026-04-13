from __future__ import annotations

from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import ProjectState


class Project(TimestampMixin, Base):
    __tablename__ = 'projects'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    teaser: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    description_markdown: Mapped[str | None] = mapped_column(Text)
    cover_image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    github_url: Mapped[str | None] = mapped_column(String(500))
    github_repo_owner: Mapped[str | None] = mapped_column(String(120))
    github_repo_name: Mapped[str | None] = mapped_column(String(120))
    demo_url: Mapped[str | None] = mapped_column(String(500))
    company_name: Mapped[str | None] = mapped_column(String(255))
    started_on: Mapped[date | None] = mapped_column(Date)
    ended_on: Mapped[date | None] = mapped_column(Date)
    duration_label: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[ProjectState] = mapped_column(SqlEnum(ProjectState, native_enum=False), nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    cover_image_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys='Project.cover_image_file_id',
        back_populates='project_cover_for',
    )
    skill_links: Mapped[list['ProjectSkill']] = relationship(back_populates='project', cascade='all, delete-orphan')
    images: Mapped[list['ProjectImage']] = relationship(
        back_populates='project', cascade='all, delete-orphan', order_by='ProjectImage.sort_order'
    )


class ProjectSkill(Base):
    __tablename__ = 'project_skills'

    project_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('projects.id', ondelete='CASCADE'), primary_key=True
    )
    skill_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True
    )

    project: Mapped[Project] = relationship(back_populates='skill_links')
    skill: Mapped['Skill'] = relationship(back_populates='project_links')


class ProjectImage(Base):
    __tablename__ = 'project_images'
    __table_args__ = (
        UniqueConstraint('project_id', 'image_file_id', name='uq_project_images_project_file'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    project_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    image_file_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('media_files.id', ondelete='SET NULL'))
    alt_text: Mapped[str | None] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_cover: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    project: Mapped[Project] = relationship(back_populates='images')
    image_file: Mapped['MediaFile | None'] = relationship(
        'MediaFile',
        foreign_keys='ProjectImage.image_file_id',
        back_populates='project_images',
    )
