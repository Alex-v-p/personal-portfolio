from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class StoredMediaObject:
    bucket_name: str
    object_key: str
    original_filename: str
    stored_filename: str
    mime_type: str | None
    file_size_bytes: int
    checksum: str


@dataclass(slots=True)
class MediaReferenceSummary:
    profile_avatar_count: int = 0
    profile_hero_count: int = 0
    profile_resume_count: int = 0
    experience_logo_count: int = 0
    project_cover_count: int = 0
    project_gallery_image_count: int = 0
    blog_cover_count: int = 0

    @property
    def total_references(self) -> int:
        return (
            self.profile_avatar_count
            + self.profile_hero_count
            + self.profile_resume_count
            + self.experience_logo_count
            + self.project_cover_count
            + self.project_gallery_image_count
            + self.blog_cover_count
        )

    @property
    def is_referenced(self) -> bool:
        return self.total_references > 0
