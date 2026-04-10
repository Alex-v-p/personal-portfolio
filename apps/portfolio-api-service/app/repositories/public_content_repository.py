from __future__ import annotations

from app.data.public_content import BLOG_POSTS, PROFILE, PROJECTS
from app.schemas.public import BlogPostOut, ProfileOut, ProjectOut


class PublicContentRepository:
    def get_profile(self) -> ProfileOut:
        return ProfileOut.model_validate(PROFILE)

    def list_projects(self) -> list[ProjectOut]:
        projects = [ProjectOut.model_validate(project) for project in PROJECTS]
        return sorted(projects, key=lambda project: (project.sort_order, project.title.lower()))

    def list_blog_posts(self) -> list[BlogPostOut]:
        posts = [BlogPostOut.model_validate(post) for post in BLOG_POSTS]
        return sorted(posts, key=lambda post: post.published_at, reverse=True)

    def get_blog_post_by_slug(self, slug: str) -> BlogPostOut | None:
        for post in BLOG_POSTS:
            if post['slug'] == slug:
                return BlogPostOut.model_validate(post)

        return None
