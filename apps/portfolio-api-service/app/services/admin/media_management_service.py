from __future__ import annotations

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.config import get_settings
from app.repositories.admin.media import AdminMediaRepository
from app.schemas.admin import AdminMediaUploadOut
from app.services.media_storage import AdminMediaStorageService
from app.services.request_protection import enforce_rate_limit_or_429


class AdminMediaManagementService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = AdminMediaRepository(session)
        self.storage = AdminMediaStorageService()
        self.settings = get_settings()

    def validate_upload_request(self, request: Request, *, admin_identifier: str, visibility: str) -> None:
        enforce_rate_limit_or_429(
            scope='admin-media-upload',
            identifier=admin_identifier,
            limit=self.settings.media_upload_rate_limit_max_requests,
            window_seconds=self.settings.media_upload_rate_limit_window_seconds,
            detail='Too many media uploads were attempted. Please wait before uploading more files.',
        )
        request_length = request.headers.get('content-length')
        if request_length and request_length.isdigit() and int(request_length) > self.settings.media_max_upload_bytes + 8192:
            raise HTTPException(status_code=413, detail='Uploaded file exceeds the configured size limit.')
        if visibility not in {'public', 'private', 'signed'}:
            raise HTTPException(status_code=400, detail='Invalid media visibility.')

    def upload_bytes(
        self,
        *,
        file_bytes: bytes,
        original_filename: str,
        mime_type: str | None,
        folder: str | None,
        title: str | None,
        alt_text: str | None,
        description: str | None,
        visibility: str,
        uploaded_by_id: UUID,
    ) -> AdminMediaUploadOut:
        if not file_bytes:
            raise HTTPException(status_code=400, detail='Uploaded file is empty.')
        if len(file_bytes) > self.settings.media_max_upload_bytes:
            raise HTTPException(status_code=413, detail='Uploaded file exceeds the configured size limit.')

        stored_object = self.storage.upload_bytes(
            file_bytes=file_bytes,
            original_filename=original_filename,
            mime_type=mime_type,
            folder=folder,
        )
        try:
            return self.repository.create_media_file(
                stored_object=stored_object,
                uploaded_by_id=uploaded_by_id,
                title=title,
                alt_text=alt_text,
                description=description,
                visibility=visibility,
            )
        except Exception:
            self.storage.delete_object(bucket_name=stored_object.bucket_name, object_key=stored_object.object_key)
            raise

    def delete_media(self, media_id: UUID) -> bool:
        media_file = self.repository.get_media_file(media_id)
        if media_file is None:
            return False
        try:
            self.storage.delete_object(bucket_name=media_file.bucket_name, object_key=media_file.object_key)
        except Exception:
            pass
        return self.repository.delete_media_file(media_id)
