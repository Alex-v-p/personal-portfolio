from __future__ import annotations

from datetime import date

from app.db.models import BlogPost, BlogPostTag, Experience, ExperienceSkill, GithubContributionDay, GithubSnapshot, Project, ProjectImage, ProjectSkill
from app.domains.admin.schema import AdminGithubSnapshotUpsertIn


class AdminRepositoryRelationshipsMixin:
    def _replace_project_skill_links(self, project: Project, skill_ids: list[str]) -> None:
        parsed_skill_ids = [self._required_uuid(skill_id) for skill_id in skill_ids if skill_id]

        project.skill_links.clear()

        for skill_id in parsed_skill_ids:
            project.skill_links.append(ProjectSkill(skill_id=skill_id))
        self.session.flush()

    def _replace_experience_skill_links(self, experience: Experience, skill_ids: list[str]) -> None:
        parsed_skill_ids = [self._required_uuid(skill_id) for skill_id in skill_ids if skill_id]

        experience.skill_links.clear()
        for skill_id in parsed_skill_ids:
            experience.skill_links.append(ExperienceSkill(skill_id=skill_id))
        self.session.flush()

    def _replace_github_contribution_days(self, snapshot: GithubSnapshot, payload: AdminGithubSnapshotUpsertIn) -> None:
        snapshot.contribution_days.clear()

        self.session.flush()

        for day in payload.contribution_days:
            snapshot.contribution_days.append(
                GithubContributionDay(
                    contribution_date=self._parse_date(day.date) or date.today(),
                    contribution_count=day.count,
                    level=day.level,
                )
            )
        self.session.flush()

    def _sync_cover_project_image(self, project: Project) -> None:

        cover_image = next((image for image in project.images if image.is_cover), None)
        if project.cover_image_file_id is None:
            if cover_image is not None:
                project.images.remove(cover_image)
            return

        if cover_image is None:
            project.images.append(
                ProjectImage(
                    image_file_id=project.cover_image_file_id,
                    alt_text=f'{project.title} cover image',
                    sort_order=0,
                    is_cover=True,
                )
            )
            return

        cover_image.image_file_id = project.cover_image_file_id
        cover_image.alt_text = cover_image.alt_text or f'{project.title} cover image'
        cover_image.sort_order = 0

    def _replace_blog_post_tags(self, post: BlogPost, tag_ids: list[str]) -> None:
        parsed_tag_ids = [self._required_uuid(tag_id) for tag_id in tag_ids if tag_id]
        post.tag_links.clear()

        self.session.flush()

        for tag_id in parsed_tag_ids:
            post.tag_links.append(BlogPostTag(tag_id=tag_id))
