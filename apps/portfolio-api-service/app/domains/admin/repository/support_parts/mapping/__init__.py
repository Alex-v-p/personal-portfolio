from .activity import AdminRepositoryActivityMappingMixin
from .blog import AdminRepositoryBlogMappingMixin
from .common import AdminRepositoryMappingCommonMixin
from .experience import AdminRepositoryExperienceMappingMixin
from .media import AdminRepositoryMediaMappingMixin
from .messages import AdminRepositoryMessagesMappingMixin
from .navigation import AdminRepositoryNavigationMappingMixin
from .profile import AdminRepositoryProfileMappingMixin
from .projects import AdminRepositoryProjectsMappingMixin
from .stats import AdminRepositoryStatsMappingMixin
from .users import AdminRepositoryUserMappingMixin


class AdminRepositoryMappingMixin(
    AdminRepositoryMappingCommonMixin,
    AdminRepositoryUserMappingMixin,
    AdminRepositoryProfileMappingMixin,
    AdminRepositoryProjectsMappingMixin,
    AdminRepositoryBlogMappingMixin,
    AdminRepositoryExperienceMappingMixin,
    AdminRepositoryNavigationMappingMixin,
    AdminRepositoryStatsMappingMixin,
    AdminRepositoryMessagesMappingMixin,
    AdminRepositoryActivityMappingMixin,
    AdminRepositoryMediaMappingMixin,
):
    pass


__all__ = ['AdminRepositoryMappingMixin']
