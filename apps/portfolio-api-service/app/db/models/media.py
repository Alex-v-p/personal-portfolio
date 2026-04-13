from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Enum as SqlEnum, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import MediaVisibility


class MediaFile(TimestampMixin, Base):
    __tablename__ = 'media_files'
    __table_args__ = (
        CheckConstraint('file_size_bytes IS NULL OR file_size_bytes >= 0', name='ck_media_files_file_size_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    bucket_name: Mapped[str] = mapped_column(String(120), nullable=False)
    object_key: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_filename: Mapped[str | None] = mapped_column(String(255))
    mime_type: Mapped[str | None] = mapped_column(String(120))
    file_size_bytes: Mapped[int | None] = mapped_column(Integer)
    checksum: Mapped[str | None] = mapped_column(String(255))
    public_url: Mapped[str | None] = mapped_column(String(500))
    alt_text: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    visibility: Mapped[MediaVisibility] = mapped_column(SqlEnum(MediaVisibility, native_enum=False), nullable=False, default=MediaVisibility.PRIVATE)
    uploaded_by_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey('admin_users.id', ondelete='SET NULL'))

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
