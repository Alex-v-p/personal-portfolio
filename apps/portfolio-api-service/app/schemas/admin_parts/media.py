from __future__ import annotations

from pydantic import Field

from app.schemas.base import ApiSchema
from app.schemas.public import PublicMediaAssetOut


class AdminMediaUsageSummaryOut(ApiSchema):
    profile_avatar_count: int = 0
    profile_hero_count: int = 0
    profile_resume_count: int = 0
    experience_logo_count: int = 0
    project_cover_count: int = 0
    project_gallery_image_count: int = 0
    blog_cover_count: int = 0
    total_references: int = 0
    is_referenced: bool = False


class AdminMediaFileOut(ApiSchema):
    id: str
    bucket_name: str
    object_key: str
    original_filename: str
    stored_filename: str | None = None
    mime_type: str | None = None
    file_size_bytes: int | None = None
    checksum: str | None = None
    description: str | None = None
    visibility: str
    alt_text: str | None = None
    title: str | None = None
    public_url: str | None = None
    folder: str | None = None
    resolved_asset: PublicMediaAssetOut | None = None
    usage_summary: AdminMediaUsageSummaryOut = Field(default_factory=AdminMediaUsageSummaryOut)
    can_delete: bool = True
    created_at: str
    updated_at: str


class AdminMediaUploadOut(AdminMediaFileOut):
    pass


__all__ = ['AdminMediaFileOut', 'AdminMediaUploadOut', 'AdminMediaUsageSummaryOut']
