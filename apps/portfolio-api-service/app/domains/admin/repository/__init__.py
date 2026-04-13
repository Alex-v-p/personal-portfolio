from app.domains.admin.repository.activity import AdminActivityRepository
from app.domains.admin.repository.content import AdminContentManagementRepository
from app.domains.admin.repository.media import AdminMediaRepository
from app.domains.admin.repository.overview import AdminOverviewRepository
from app.domains.admin.repository.stats import AdminGithubRepository
from app.domains.admin.repository.taxonomy import AdminTaxonomyRepository
from app.domains.admin.repository.users import AdminUsersRepository

__all__ = [
    "AdminActivityRepository",
    "AdminContentManagementRepository",
    "AdminGithubRepository",
    "AdminMediaRepository",
    "AdminOverviewRepository",
    "AdminTaxonomyRepository",
    "AdminUsersRepository",
]
