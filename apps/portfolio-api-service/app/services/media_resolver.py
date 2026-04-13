from __future__ import annotations

from app.core.config import get_settings
from app.db.models import MediaFile, MediaVisibility


class PublicMediaUrlResolver:
    def __init__(self, *, allow_non_public: bool = False) -> None:
        self.settings = get_settings()
        self.allow_non_public = allow_non_public

    def resolve(self, media_file: MediaFile | None) -> str | None:
        if media_file is None:
            return None

        if not self.allow_non_public and media_file.visibility is not MediaVisibility.PUBLIC:
            return None

        object_key = (media_file.object_key or '').lstrip('/')
        if object_key and media_file.bucket_name:
            base_url = self.settings.media_public_base_url.rstrip('/')
            return f'{base_url}/{media_file.bucket_name}/{object_key}'

        if media_file.public_url:
            return media_file.public_url

        return None
