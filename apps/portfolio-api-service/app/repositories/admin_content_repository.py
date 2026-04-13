from __future__ import annotations

from app.repositories.admin import (
    AdminActivityRepository,
    AdminContentManagementRepository,
    AdminGithubRepository,
    AdminMediaRepository,
    AdminOverviewRepository,
    AdminTaxonomyRepository,
    AdminUsersRepository,
)


class AdminContentRepository(
    AdminUsersRepository,
    AdminOverviewRepository,
    AdminMediaRepository,
    AdminTaxonomyRepository,
    AdminContentManagementRepository,
    AdminGithubRepository,
    AdminActivityRepository,
):
    """Compatibility facade that preserves the original repository API.

    New code should prefer importing narrower domain-specific repositories from
    ``app.repositories.admin``.
    """

    pass
