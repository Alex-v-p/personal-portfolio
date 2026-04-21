from __future__ import annotations

from sqlalchemy.orm import Session

from app.domains.media.resolver import PublicMediaUrlResolver
from .blog import PublicBlogRepositoryMixin
from .common import DEFAULT_PUBLIC_LOCALE, PublicLocale, PublicRepositoryCommonMixin
from .experience import PublicExperienceRepositoryMixin
from .overview import PublicOverviewRepositoryMixin
from .profile import PublicProfileRepositoryMixin
from .projects import PublicProjectsRepositoryMixin
from .stats import PublicStatsRepositoryMixin


class PublicContentRepository(
    PublicRepositoryCommonMixin,
    PublicProfileRepositoryMixin,
    PublicProjectsRepositoryMixin,
    PublicBlogRepositoryMixin,
    PublicExperienceRepositoryMixin,
    PublicOverviewRepositoryMixin,
    PublicStatsRepositoryMixin,
):
    def __init__(
        self,
        session: Session,
        media_resolver: PublicMediaUrlResolver | None = None,
        *,
        locale: PublicLocale = DEFAULT_PUBLIC_LOCALE,
    ) -> None:
        self.session = session
        self.media_resolver = media_resolver or PublicMediaUrlResolver()
        self.locale = locale


__all__ = [
    'DEFAULT_PUBLIC_LOCALE',
    'PublicBlogRepositoryMixin',
    'PublicContentRepository',
    'PublicLocale',
    'PublicRepositoryCommonMixin',
    'PublicExperienceRepositoryMixin',
    'PublicOverviewRepositoryMixin',
    'PublicProfileRepositoryMixin',
    'PublicProjectsRepositoryMixin',
    'PublicStatsRepositoryMixin',
]
