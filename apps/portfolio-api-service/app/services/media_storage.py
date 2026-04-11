from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re
from uuid import uuid4

import boto3
from botocore.client import Config

from app.core.config import get_settings

_folder_pattern = re.compile(r'[^a-zA-Z0-9._/-]+')
_filename_pattern = re.compile(r'[^a-zA-Z0-9._-]+')


@dataclass(slots=True)
class StoredMediaObject:
    bucket_name: str
    object_key: str
    original_filename: str
    stored_filename: str
    mime_type: str | None
    file_size_bytes: int
    checksum: str


class AdminMediaStorageService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = boto3.client(
            's3',
            endpoint_url=self.settings.media_storage_endpoint,
            aws_access_key_id=self.settings.media_storage_access_key,
            aws_secret_access_key=self.settings.media_storage_secret_key,
            region_name=self.settings.media_storage_region,
            config=Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
        )

    def upload_bytes(
        self,
        *,
        file_bytes: bytes,
        original_filename: str,
        mime_type: str | None,
        folder: str | None = None,
    ) -> StoredMediaObject:
        safe_original = self._sanitize_filename(original_filename)
        safe_folder = self._sanitize_folder(folder)
        extension = Path(safe_original).suffix.lower()[:20] if Path(safe_original).suffix else ''
        stored_filename = f'{uuid4().hex}{extension}'
        object_key = f'{safe_folder}/{stored_filename}' if safe_folder else stored_filename

        put_kwargs: dict[str, object] = {
            'Bucket': self.settings.media_public_bucket,
            'Key': object_key,
            'Body': file_bytes,
        }
        if mime_type:
            put_kwargs['ContentType'] = mime_type
        self.client.put_object(**put_kwargs)

        return StoredMediaObject(
            bucket_name=self.settings.media_public_bucket,
            object_key=object_key,
            original_filename=safe_original,
            stored_filename=stored_filename,
            mime_type=mime_type,
            file_size_bytes=len(file_bytes),
            checksum=sha256(file_bytes).hexdigest(),
        )

    def delete_object(self, *, bucket_name: str, object_key: str) -> None:
        self.client.delete_object(Bucket=bucket_name, Key=object_key)

    def _sanitize_folder(self, value: str | None) -> str:
        raw = (value or 'uploads').strip().strip('/')
        cleaned = _folder_pattern.sub('-', raw)
        collapsed = '/'.join(part for part in cleaned.split('/') if part and part != '.')
        return collapsed[:200] or 'uploads'

    def _sanitize_filename(self, value: str) -> str:
        raw = Path(value or 'upload').name.strip()
        cleaned = _filename_pattern.sub('-', raw)
        return (cleaned or 'upload')[:255]
