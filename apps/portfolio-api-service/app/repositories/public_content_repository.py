from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.public import (
    PublicBlogRepositoryMixin,
    PublicExperienceRepositoryMixin,
    PublicOverviewRepositoryMixin,
    PublicProfileRepositoryMixin,
    PublicProjectsRepositoryMixin,
    PublicRepositoryCommonMixin,
    PublicStatsRepositoryMixin,
)
from app.services.media_resolver import PublicMediaUrlResolver


class PublicContentRepository(
    PublicOverviewRepositoryMixin,
    PublicProfileRepositoryMixin,
    PublicProjectsRepositoryMixin,
    PublicBlogRepositoryMixin,
    PublicExperienceRepositoryMixin,
    PublicStatsRepositoryMixin,
    PublicRepositoryCommonMixin,
):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.media_resolver = PublicMediaUrlResolver()
