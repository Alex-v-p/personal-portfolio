from __future__ import annotations

from app.schemas.base import ApiSchema
from app.domains.admin.schema_parts.common import ProjectStateLiteral, PublicationStatusLiteral
from app.domains.admin.schema_parts.media import AdminMediaFileOut
from app.domains.admin.schema_parts.taxonomy import AdminBlogTagOut, AdminSkillCategoryOut, AdminSkillOut


class AdminReferenceDataOut(ApiSchema):
    skills: list[AdminSkillOut]
    skill_categories: list[AdminSkillCategoryOut]
    media_files: list[AdminMediaFileOut]
    blog_tags: list[AdminBlogTagOut]
    project_states: list[ProjectStateLiteral]
    publication_statuses: list[PublicationStatusLiteral]


class AdminDashboardSummaryOut(ApiSchema):
    projects: int
    blog_posts: int
    unread_messages: int
    skills: int
    skill_categories: int
    media_files: int
    experiences: int
    navigation_items: int
    blog_tags: int
    admin_users: int
    github_snapshots: int


__all__ = ['AdminDashboardSummaryOut', 'AdminReferenceDataOut']
