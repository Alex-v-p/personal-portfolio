from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from pathlib import PurePosixPath
from uuid import uuid4

from minio import Minio

from app.core.config import get_settings


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
        settings = get_settings()
        self.bucket_name = settings.media_public_bucket
        self.client = Minio(
            settings.media_storage_endpoint,
            access_key=settings.media_storage_access_key,
            secret_key=settings.media_storage_secret_key,
            secure=settings.media_storage_secure,
        )

    def upload_bytes(self, *, file_bytes: bytes, original_filename: str, mime_type: str | None, folder: str | None = None) -> StoredMediaObject:
        checksum = sha256(file_bytes).hexdigest()
        folder_path = PurePosixPath((folder or '').strip('/'))
        suffix = PurePosixPath(original_filename).suffix.lower()
        stored_filename = f'{uuid4().hex}{suffix}'
        object_key = str(folder_path / stored_filename) if str(folder_path) not in {'', '.'} else stored_filename
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_key,
            data=BytesIO(file_bytes),
            length=len(file_bytes),
            content_type=mime_type or 'application/octet-stream',
        )
        return StoredMediaObject(
            bucket_name=self.bucket_name,
            object_key=object_key,
            original_filename=PurePosixPath(original_filename).name or 'upload',
            stored_filename=stored_filename,
            mime_type=mime_type,
            file_size_bytes=len(file_bytes),
            checksum=checksum,
        )

    def delete_object(self, *, bucket_name: str, object_key: str) -> None:
        self.client.remove_object(bucket_name=bucket_name, object_name=object_key)
