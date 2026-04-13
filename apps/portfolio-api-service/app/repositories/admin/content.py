from __future__ import annotations

from app.repositories.admin.content_parts import (
    AdminBlogContentRepository,
    AdminExperienceContentRepository,
    AdminNavigationContentRepository,
    AdminProfileContentRepository,
    AdminProjectContentRepository,
)
from app.repositories.admin.support import AdminRepositorySupport


class AdminContentManagementRepository(
    AdminProjectContentRepository,
    AdminBlogContentRepository,
    AdminExperienceContentRepository,
    AdminNavigationContentRepository,
    AdminProfileContentRepository,
    AdminRepositorySupport,
):
    pass
