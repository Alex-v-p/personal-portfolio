from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.repositories.admin.media import AdminMediaRepository
from app.services.media.references import AdminMediaReferenceService
from app.services.media.storage import AdminMediaStorageService
from app.services.media.validation import AdminMediaUploadRequestValidator


class AdminMediaManagementService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = AdminMediaRepository(session)
        self.storage = AdminMediaStorageService()
        self.validator = AdminMediaUploadRequestValidator()
        self.references = AdminMediaReferenceService(session)

    def validate_upload_request(self, request: Request, *, admin_identifier: str, visibility: str) -> None:
        self.validator.validate_request(request, admin_identifier=admin_identifier, visibility=visibility)

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
    ):
        self.validator.validate_payload(file_bytes=file_bytes, original_filename=original_filename)
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
        usage = self.references.get_usage_for_media(media_file)
        if usage.is_referenced:
            raise HTTPException(
                status_code=409,
                detail='This media file is still referenced by portfolio content. Remove those references before deleting it.',
            )
        try:
            self.storage.delete_object(bucket_name=media_file.bucket_name, object_key=media_file.object_key)
        except Exception:
            pass
        return self.repository.delete_media_file(media_id)
