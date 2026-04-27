from __future__ import annotations

from collections import defaultdict
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import BlogPost, Experience, MediaFile, Profile, Project, ProjectImage
from app.domains.media.service.models import MediaReferenceSummary


class AdminMediaReferenceService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def build_usage_map(self, media_ids: list[UUID] | None = None) -> dict[UUID, MediaReferenceSummary]:
        usage_map: dict[UUID, MediaReferenceSummary] = defaultdict(MediaReferenceSummary)
        for model, column, attribute in (
            (Profile, Profile.avatar_file_id, 'profile_avatar_count'),
            (Profile, Profile.hero_image_file_id, 'profile_hero_count'),
            (Profile, Profile.resume_file_id, 'profile_resume_count'),
            (Profile, Profile.resume_file_id_nl, 'profile_resume_count'),
            (Experience, Experience.logo_file_id, 'experience_logo_count'),
            (Project, Project.cover_image_file_id, 'project_cover_count'),
            (ProjectImage, ProjectImage.image_file_id, 'project_gallery_image_count'),
            (BlogPost, BlogPost.cover_image_file_id, 'blog_cover_count'),
        ):
            statement = select(column, func.count()).where(column.is_not(None)).group_by(column)
            if media_ids:
                statement = statement.where(column.in_(media_ids))
            for media_id, count in self.session.execute(statement).all():
                if media_id is None:
                    continue
                current_count = getattr(usage_map[media_id], attribute)
                setattr(usage_map[media_id], attribute, current_count + int(count))
        return dict(usage_map)

    def get_usage_for_media(self, media_file: MediaFile) -> MediaReferenceSummary:
        return self.build_usage_map([media_file.id]).get(media_file.id, MediaReferenceSummary())
