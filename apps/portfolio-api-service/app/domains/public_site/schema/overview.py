from __future__ import annotations

from app.schemas.base import ApiSchema

from .blog import BlogPostSummaryOut
from .experience import ExperienceOut
from .profile import ContactMethodOut, ExpertiseGroupOut, ProfileOut
from .projects import ProjectSummaryOut


class HomeOut(ApiSchema):
    hero: ProfileOut
    featured_projects: list[ProjectSummaryOut]
    featured_blog_posts: list[BlogPostSummaryOut]
    expertise_groups: list[ExpertiseGroupOut]
    experience_preview: list[ExperienceOut]
    contact_preview: list[ContactMethodOut]


__all__ = ['HomeOut']
