from __future__ import annotations

from urllib.parse import quote

from app.core.config import get_settings
from app.db.models import MediaFile


class PublicMediaUrlResolver:
    def __init__(self) -> None:
        self.settings = get_settings()

    def resolve(self, media_file: MediaFile | None) -> str | None:
        if media_file is None:
            return None

        object_key = media_file.object_key.lstrip('/')
        if self.settings.media_public_base_url and media_file.bucket_name and object_key:
            base_url = self.settings.media_public_base_url.rstrip('/')
            encoded_object_key = quote(object_key, safe='/')
            return f'{base_url}/{media_file.bucket_name}/{encoded_object_key}'

        if media_file.public_url:
            return media_file.public_url

        return f'/media/{object_key}' if object_key else None
