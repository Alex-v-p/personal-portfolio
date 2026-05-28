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
        self._replace_project_images(project, [])

    def _replace_project_images(self, project: Project, images_payload) -> None:
        """Replace the project gallery while keeping the selected cover image as the first gallery item."""
        cover_file_id = project.cover_image_file_id
        cover_payload = None
        gallery_payloads = []
        seen_file_ids: set[str] = set()

        for image_payload in images_payload or []:
            image_file_id = self._optional_uuid(getattr(image_payload, 'image_file_id', None))
            if image_file_id is None:
                continue
            image_file_key = str(image_file_id)
            if image_file_key in seen_file_ids:
                continue
            seen_file_ids.add(image_file_key)

            if bool(getattr(image_payload, 'is_cover', False)) or (cover_file_id is not None and image_file_id == cover_file_id):
                cover_payload = image_payload
                cover_file_id = image_file_id
                continue

            gallery_payloads.append(image_payload)

        if cover_file_id is not None:
            project.cover_image_file_id = cover_file_id

        project.images.clear()
        self.session.flush()

        sort_order = 0
        if project.cover_image_file_id is not None:
            project.images.append(
                ProjectImage(
                    image_file_id=project.cover_image_file_id,
                    alt_text=(self._normalize_optional_text(getattr(cover_payload, 'alt_text', None)) if cover_payload else None) or f'{project.title} cover image',
                    alt_text_nl=self._normalize_optional_text(getattr(cover_payload, 'alt_text_nl', None)) if cover_payload else None,
                    sort_order=sort_order,
                    is_cover=True,
                )
            )
            sort_order += 1

        for image_payload in sorted(gallery_payloads, key=lambda item: getattr(item, 'sort_order', 0)):
            image_file_id = self._optional_uuid(getattr(image_payload, 'image_file_id', None))
            if image_file_id is None or image_file_id == project.cover_image_file_id:
                continue
            project.images.append(
                ProjectImage(
                    image_file_id=image_file_id,
                    alt_text=self._normalize_optional_text(getattr(image_payload, 'alt_text', None)),
                    alt_text_nl=self._normalize_optional_text(getattr(image_payload, 'alt_text_nl', None)),
                    sort_order=sort_order,
                    is_cover=False,
                )
            )
            sort_order += 1

        self.session.flush()

    def _replace_blog_post_tags(self, post: BlogPost, tag_ids: list[str]) -> None:
        parsed_tag_ids = [self._required_uuid(tag_id) for tag_id in tag_ids if tag_id]
        post.tag_links.clear()

        self.session.flush()

        for tag_id in parsed_tag_ids:
            post.tag_links.append(BlogPostTag(tag_id=tag_id))
