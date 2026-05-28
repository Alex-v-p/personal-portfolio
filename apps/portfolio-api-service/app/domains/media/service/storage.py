from __future__ import annotations

from hashlib import sha256
from io import BytesIO
from pathlib import PurePosixPath
from typing import Any
from uuid import uuid4

from app.core.config import get_settings
from app.domains.media.service.models import StoredMediaObject

try:  # pragma: no cover - exercised indirectly when optional dependency is installed
    from minio import Minio as _MinioClient
except ModuleNotFoundError:  # pragma: no cover - allows non-upload tests to import this module
    _MinioClient = None


class AdminMediaStorageService:
    def __init__(self) -> None:
        settings = get_settings()
        self.bucket_name = settings.media_public_bucket
        self.client = self._build_client(
            endpoint=settings.media_storage_endpoint,
            access_key=settings.media_storage_access_key,
            secret_key=settings.media_storage_secret_key,
            secure=settings.media_storage_secure,
        )

    @staticmethod
    def _build_client(*, endpoint: str, access_key: str, secret_key: str, secure: bool) -> Any:
        if _MinioClient is None:
            raise RuntimeError(
                'The optional "minio" package is required for media upload and deletion operations. '
                'Install portfolio-api-service requirements before using AdminMediaStorageService.'
            )
        return _MinioClient(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
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

    def download_object(self, *, bucket_name: str, object_key: str) -> bytes:
        response = self.client.get_object(bucket_name=bucket_name, object_name=object_key)
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    def delete_object(self, *, bucket_name: str, object_key: str) -> None:
        self.client.remove_object(bucket_name=bucket_name, object_name=object_key)
