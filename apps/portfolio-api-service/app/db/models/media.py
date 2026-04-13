from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import MediaVisibility


class MediaFile(TimestampMixin, Base):
    __tablename__ = 'media_files'
    __table_args__ = (
        UniqueConstraint('object_key', name='uq_media_files_object_key'),
        CheckConstraint('byte_size >= 0', name='ck_media_files_byte_size_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    object_key: Mapped[str] = mapped_column(String(500), nullable=False)
    bucket_name: Mapped[str] = mapped_column(String(120), nullable=False)
    media_kind: Mapped[str] = mapped_column(String(80), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(120), nullable=False)
    extension: Mapped[str | None] = mapped_column(String(20))
    byte_size: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)
    alt_text: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    folder: Mapped[str | None] = mapped_column(String(255))
    visibility: Mapped[MediaVisibility] = mapped_column(SqlEnum(MediaVisibility, native_enum=False), nullable=False, default=MediaVisibility.PRIVATE)
    checksum_sha256: Mapped[str | None] = mapped_column(String(128))
    uploaded_by_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('admin_users.id', ondelete='SET NULL'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    uploaded_by: Mapped['AdminUser | None'] = relationship(back_populates='uploaded_media_files')
    profile_avatar_for: Mapped[list['Profile']] = relationship(
        'Profile',
        foreign_keys='Profile.avatar_file_id',
        back_populates='avatar_file',
    )
    profile_hero_for: Mapped[list['Profile']] = relationship(
        'Profile',
        foreign_keys='Profile.hero_image_file_id',
        back_populates='hero_image_file',
    )
    profile_resume_for: Mapped[list['Profile']] = relationship(
        'Profile',
        foreign_keys='Profile.resume_file_id',
        back_populates='resume_file',
    )
    experience_logo_for: Mapped[list['Experience']] = relationship(
        'Experience',
        foreign_keys='Experience.logo_file_id',
        back_populates='logo_file',
    )
    project_cover_for: Mapped[list['Project']] = relationship(
        'Project',
        foreign_keys='Project.cover_image_file_id',
        back_populates='cover_image_file',
    )
    project_images: Mapped[list['ProjectImage']] = relationship(
        'ProjectImage',
        foreign_keys='ProjectImage.image_file_id',
        back_populates='image_file',
    )
    blog_cover_for: Mapped[list['BlogPost']] = relationship(
        'BlogPost',
        foreign_keys='BlogPost.cover_image_file_id',
        back_populates='cover_image_file',
    )
