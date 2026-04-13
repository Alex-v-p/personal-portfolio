from app.repositories.admin.activity import AdminActivityRepository
from app.repositories.admin.content import AdminContentManagementRepository
from app.repositories.admin.media import AdminMediaRepository
from app.repositories.admin.overview import AdminOverviewRepository
from app.repositories.admin.stats import AdminGithubRepository
from app.repositories.admin.taxonomy import AdminTaxonomyRepository
from app.repositories.admin.users import AdminUsersRepository

__all__ = [
    "AdminActivityRepository",
    "AdminContentManagementRepository",
    "AdminGithubRepository",
    "AdminMediaRepository",
    "AdminOverviewRepository",
    "AdminTaxonomyRepository",
    "AdminUsersRepository",
]
