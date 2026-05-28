from __future__ import annotations

from pathlib import PurePosixPath
from uuid import UUID

from app.core.config import get_settings
from app.db.models import MediaFile, MediaVisibility


class PublicMediaUrlResolver:
    def __init__(self, *, allow_non_public: bool = False) -> None:
        self.settings = get_settings()
        self.allow_non_public = allow_non_public

    def resolve(self, media_file: MediaFile | None) -> str | None:
        if media_file is None:
            return None

        if not self.allow_non_public and media_file.visibility != MediaVisibility.PUBLIC:
            return None

        object_key = (media_file.object_key or '').lstrip('/')
        if object_key and media_file.bucket_name:
            base_url = self.settings.media_public_base_url.rstrip('/')
            return f'{base_url}/{media_file.bucket_name}/{object_key}'

        return media_file.public_url

    def resolve_download(self, media_file: MediaFile | None) -> str | None:
        if media_file is None or media_file.visibility != MediaVisibility.PUBLIC:
            return None

        return build_public_download_url(media_file.id, media_file.original_filename or media_file.stored_filename or media_file.object_key)


def build_public_download_url(media_id: UUID | str, filename: str | None) -> str:
    safe_filename = sanitize_public_download_filename(filename)
    return f'/api/public/media-files/{media_id}/{safe_filename}'


def sanitize_public_download_filename(filename: str | None) -> str:
    raw_name = PurePosixPath(filename or '').name.strip() or 'download'
    cleaned = ''.join(character if character.isalnum() or character in {'-', '_', '.', ' '} else '-' for character in raw_name).strip('. ')
    return cleaned or 'download'
