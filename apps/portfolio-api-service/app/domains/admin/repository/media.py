from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from app.db.models import MediaFile, MediaVisibility
from app.domains.admin.schema import AdminMediaFileOut, AdminMediaUsageSummaryOut
from app.domains.admin.repository.support import AdminRepositorySupport
from app.domains.media.service.models import MediaReferenceSummary, StoredMediaObject
from app.domains.media.service.references import AdminMediaReferenceService


class AdminMediaRepository(AdminRepositorySupport):
    def list_media_files(self) -> list[AdminMediaFileOut]:
        media_files = self.session.scalars(select(MediaFile).order_by(MediaFile.created_at.desc())).all()
        usage_map = AdminMediaReferenceService(self.session).build_usage_map([media_file.id for media_file in media_files])
        return [self._map_media_file(media_file, self._map_usage_summary(usage_map.get(media_file.id))) for media_file in media_files]

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
        return self._map_media_file(media_file, AdminMediaUsageSummaryOut())

    def get_media_file(self, media_id: UUID) -> MediaFile | None:
        return self.session.get(MediaFile, media_id)

    def delete_media_file(self, media_id: UUID) -> bool:
        media_file = self.session.get(MediaFile, media_id)
        if media_file is None:
            return False
        self.session.delete(media_file)
        self.session.commit()
        return True

    def _map_usage_summary(self, usage: MediaReferenceSummary | None) -> AdminMediaUsageSummaryOut:
        usage = usage or MediaReferenceSummary()
        return AdminMediaUsageSummaryOut(
            profile_avatar_count=usage.profile_avatar_count,
            profile_hero_count=usage.profile_hero_count,
            profile_resume_count=usage.profile_resume_count,
            experience_logo_count=usage.experience_logo_count,
            project_cover_count=usage.project_cover_count,
            project_gallery_image_count=usage.project_gallery_image_count,
            blog_cover_count=usage.blog_cover_count,
            total_references=usage.total_references,
            is_referenced=usage.is_referenced,
        )
