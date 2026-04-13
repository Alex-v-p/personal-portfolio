from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from app.db.models import MediaFile, MediaVisibility
from app.schemas.admin import AdminMediaFileOut
from app.repositories.admin.support import AdminRepositorySupport
from app.services.media_storage import StoredMediaObject


class AdminMediaRepository(AdminRepositorySupport):
    def list_media_files(self) -> list[AdminMediaFileOut]:
        media_files = self.session.scalars(select(MediaFile).order_by(MediaFile.created_at.desc())).all()
        return [self._map_media_file(media_file) for media_file in media_files]

    def create_media_file(
        self,
        *,
        stored_object: StoredMediaObject,
        uploaded_by_id: UUID,
        title: str | None,
        alt_text: str | None,
        description: str | None,
        visibility: str,
    ) -> AdminMediaFileOut:
        media_file = MediaFile(
            bucket_name=stored_object.bucket_name,
            object_key=stored_object.object_key,
            original_filename=stored_object.original_filename,
            stored_filename=stored_object.stored_filename,
            mime_type=stored_object.mime_type,
            file_size_bytes=stored_object.file_size_bytes,
            checksum=stored_object.checksum,
            public_url=None,
            alt_text=self._normalize_optional_text(alt_text),
            title=self._normalize_optional_text(title),
            description=self._normalize_optional_text(description),
            visibility=MediaVisibility(visibility),
            uploaded_by_id=uploaded_by_id,
        )
        self.session.add(media_file)
        self.session.commit()
        self.session.refresh(media_file)
        return self._map_media_file(media_file)

    def get_media_file(self, media_id: UUID) -> MediaFile | None:
        return self.session.get(MediaFile, media_id)

    def delete_media_file(self, media_id: UUID) -> bool:
        media_file = self.session.get(MediaFile, media_id)
        if media_file is None:
            return False
        self.session.delete(media_file)
        self.session.commit()
        return True
