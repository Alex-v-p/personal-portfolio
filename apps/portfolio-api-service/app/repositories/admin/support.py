from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.admin.support_parts import (
    AdminRepositoryActivityMixin,
    AdminRepositoryMappingMixin,
    AdminRepositoryParsingMixin,
    AdminRepositoryRelationshipsMixin,
)
from app.services.media_resolver import PublicMediaUrlResolver


class AdminRepositorySupport(
    AdminRepositoryActivityMixin,
    AdminRepositoryMappingMixin,
    AdminRepositoryParsingMixin,
    AdminRepositoryRelationshipsMixin,
):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.media_resolver = PublicMediaUrlResolver(allow_non_public=True)
