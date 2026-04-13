from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.db.models import BlogPost, MediaFile, Project, ProjectState, PublicationStatus
from app.schemas.public import PublicMediaAssetOut
from app.services.media_resolver import PublicMediaUrlResolver

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class PublicRepositoryCommonMixin:
    session: Session
    media_resolver: PublicMediaUrlResolver

    @staticmethod
    def _publication_cutoff() -> datetime:
        return datetime.now(UTC)

    def _public_project_query(self):
        return select(Project).where(
            Project.state != ProjectState.ARCHIVED,
            Project.published_at <= self._publication_cutoff(),
        )

    def _public_blog_post_query(self):
        return select(BlogPost).where(
            BlogPost.status == PublicationStatus.PUBLISHED,
            BlogPost.published_at.is_not(None),
            BlogPost.published_at <= self._publication_cutoff(),
        )

    def _map_media(self, media_file: MediaFile | None, alt: str | None = None) -> PublicMediaAssetOut | None:
        url = self.media_resolver.resolve(media_file)
        if media_file is None or url is None:
            return None
        return PublicMediaAssetOut(
            id=str(media_file.id),
            url=url,
            alt=alt or media_file.alt_text,
            file_name=media_file.original_filename,
            mime_type=media_file.mime_type,
            width=None,
            height=None,
        )
