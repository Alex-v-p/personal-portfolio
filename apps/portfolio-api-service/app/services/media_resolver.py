from __future__ import annotations

from app.db.models import MediaFile


class PublicMediaUrlResolver:
    def resolve(self, media_file: MediaFile | None) -> str | None:
        if media_file is None:
            return None
        if media_file.public_url:
            return media_file.public_url
        object_key = media_file.object_key.lstrip('/')
        return f'/media/{object_key}' if object_key else None
