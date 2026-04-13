from __future__ import annotations

from app.schemas.base import ApiSchema
from app.schemas.public import PublicMediaAssetOut


class AdminMediaFileOut(ApiSchema):
    id: str
    bucket_name: str
    object_key: str
    original_filename: str
    mime_type: str | None = None
    visibility: str
    alt_text: str | None = None
    title: str | None = None
    public_url: str | None = None
    resolved_asset: PublicMediaAssetOut | None = None
    created_at: str
    updated_at: str


class AdminMediaUploadOut(AdminMediaFileOut):
    pass


__all__ = ['AdminMediaFileOut', 'AdminMediaUploadOut']
