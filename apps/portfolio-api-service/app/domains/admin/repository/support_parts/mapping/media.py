from __future__ import annotations

from app.db.models import MediaFile
from app.domains.admin.schema import AdminMediaFileOut, AdminMediaUsageSummaryOut


class AdminRepositoryMediaMappingMixin:
    def _map_media_file(self, media_file: MediaFile, usage_summary: AdminMediaUsageSummaryOut | None = None) -> AdminMediaFileOut:
        resolved_usage = usage_summary or AdminMediaUsageSummaryOut()
        return AdminMediaFileOut(
            id=str(media_file.id),
            bucket_name=media_file.bucket_name,
            object_key=media_file.object_key,
            original_filename=media_file.original_filename,
            stored_filename=media_file.stored_filename,
            mime_type=media_file.mime_type,
            file_size_bytes=media_file.file_size_bytes,
            checksum=media_file.checksum,
            description=media_file.description,
            visibility=media_file.visibility.value,
            alt_text=media_file.alt_text,
            title=media_file.title,
            public_url=media_file.public_url,
            folder=self._media_folder(media_file),
            resolved_asset=self._map_media(media_file, alt=media_file.alt_text),
            usage_summary=resolved_usage,
            can_delete=not resolved_usage.is_referenced,
            created_at=media_file.created_at.isoformat(),
            updated_at=media_file.updated_at.isoformat(),
        )
