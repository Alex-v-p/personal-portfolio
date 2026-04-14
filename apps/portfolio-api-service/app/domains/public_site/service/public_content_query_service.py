from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.public_site.repository import PublicContentRepository
from app.domains.public_site.schema import (
    BlogPostDetailOut,
    BlogPostsListOut,
    ExperienceListOut,
    GithubSnapshotOut,
    HomeOut,
    NavigationListOut,
    ProfileOut,
    ProjectDetailOut,
    ProjectsListOut,
    SiteShellOut,
    StatsOut,
)


class PublicContentQueryService:
    def __init__(self, session: Session) -> None:
        self.repository = PublicContentRepository(session)

    def get_profile(self) -> ProfileOut:
        return self._require(self.repository.get_profile(), 'Public profile not found.')

    def list_navigation(self) -> NavigationListOut:
        items = self.repository.list_navigation()
        return NavigationListOut(items=items, total=len(items))

    def get_site_shell(self) -> SiteShellOut:
        return self._require(self.repository.get_site_shell(), 'Site shell not found.')

    def get_home(self) -> HomeOut:
        return self._require(self.repository.get_home(), 'Public home content not found.')

    def list_projects(self) -> ProjectsListOut:
        items = self.repository.list_projects()
        return ProjectsListOut(items=items, total=len(items))

    def get_project(self, slug: str) -> ProjectDetailOut:
        return self._require(self.repository.get_project_by_slug(slug), 'Project not found.')

    def list_blog_posts(self) -> BlogPostsListOut:
        items = self.repository.list_blog_posts()
        return BlogPostsListOut(items=items, total=len(items))

    def get_blog_post(self, slug: str) -> BlogPostDetailOut:
        return self._require(self.repository.get_blog_post_by_slug(slug), 'Blog post not found.')

    def list_experience(self) -> ExperienceListOut:
        items = self.repository.list_experience()
        return ExperienceListOut(items=items, total=len(items))

    def get_github_snapshot(self) -> GithubSnapshotOut:
        return self._require(self.repository.get_latest_github_snapshot(), 'GitHub snapshot not found.')

    def get_stats(self) -> StatsOut:
        return self.repository.get_stats()

    @staticmethod
    def _require(value, detail: str):
        if value is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        return value
