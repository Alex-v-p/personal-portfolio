from __future__ import annotations

from app.domains.admin.repository.content_parts import (
    AdminBlogContentRepository,
    AdminExperienceContentRepository,
    AdminNavigationContentRepository,
    AdminProfileContentRepository,
    AdminProjectContentRepository,
)
from app.domains.admin.repository.support import AdminRepositorySupport


class AdminContentManagementRepository(
    AdminProjectContentRepository,
    AdminBlogContentRepository,
    AdminExperienceContentRepository,
    AdminNavigationContentRepository,
    AdminProfileContentRepository,
    AdminRepositorySupport,
):
    pass
