from __future__ import annotations

from pathlib import PurePosixPath

from fastapi import HTTPException, Request

from app.core.config import get_settings

_ALLOWED_VISIBILITY = {'public', 'private', 'signed'}


class AdminMediaUploadRequestValidator:
    def __init__(self) -> None:
        self.settings = get_settings()

    def validate_request(self, request: Request, *, admin_identifier: str, visibility: str) -> None:
        from app.services.request_protection import enforce_rate_limit_or_429

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
        if visibility not in _ALLOWED_VISIBILITY:
            raise HTTPException(status_code=400, detail='Invalid media visibility.')

    def validate_payload(self, *, file_bytes: bytes, original_filename: str) -> None:
        if not file_bytes:
            raise HTTPException(status_code=400, detail='Uploaded file is empty.')
        if len(file_bytes) > self.settings.media_max_upload_bytes:
            raise HTTPException(status_code=413, detail='Uploaded file exceeds the configured size limit.')
        cleaned_name = PurePosixPath(original_filename).name.strip()
        if not cleaned_name:
            raise HTTPException(status_code=400, detail='Uploaded file is missing a valid filename.')
