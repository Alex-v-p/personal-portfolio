from __future__ import annotations

from app.schemas.base import ApiSchema


class PublicMediaAssetOut(ApiSchema):
    id: str
    url: str
    alt: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    width: int | None = None
    height: int | None = None


__all__ = ['PublicMediaAssetOut']
