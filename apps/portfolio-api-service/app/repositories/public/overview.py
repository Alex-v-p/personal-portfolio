from __future__ import annotations

from app.schemas.public import HomeOut


class PublicOverviewRepositoryMixin:
    def get_home(self) -> HomeOut | None:
        profile = self.get_profile()
        if profile is None:
            return None
        return HomeOut(
            hero=profile,
            featured_projects=self._list_featured_projects(limit=2),
            featured_blog_posts=self._list_featured_blog_posts(limit=2),
            expertise_groups=profile.expertise_groups,
            experience_preview=self._list_experience_preview(limit=3),
            contact_preview=self._build_contact_methods(profile)[:4],
        )
