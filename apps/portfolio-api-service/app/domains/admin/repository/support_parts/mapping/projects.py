from __future__ import annotations

from app.db.models import Project, ProjectImage
from app.domains.admin.schema import AdminProjectImageOut, AdminProjectOut


class AdminRepositoryProjectsMappingMixin:
    def _map_project(self, project: Project) -> AdminProjectOut:
        ordered_skills = sorted(project.skill_links, key=lambda link: (link.skill.sort_order, link.skill.name.lower()))
        ordered_images = sorted(project.images, key=lambda image: (image.sort_order, str(image.id)))

        return AdminProjectOut(
            id=str(project.id),
            slug=project.slug,
            title=project.title,
            title_nl=project.title_nl,
            teaser=project.teaser,
            teaser_nl=project.teaser_nl,
            summary=project.summary,
            summary_nl=project.summary_nl,
            description_markdown=project.description_markdown,
            description_markdown_nl=project.description_markdown_nl,
            cover_image_file_id=str(project.cover_image_file_id) if project.cover_image_file_id else None,
            cover_image=self._map_media(project.cover_image_file, alt=f'{project.title} cover image'),
            github_url=project.github_url,
            github_repo_owner=project.github_repo_owner,
            github_repo_name=project.github_repo_name,
            demo_url=project.demo_url,
            company_name=project.company_name,
            started_on=project.started_on.isoformat() if project.started_on else None,
            ended_on=project.ended_on.isoformat() if project.ended_on else None,
            duration_label=project.duration_label,
            duration_label_nl=project.duration_label_nl,
            status=project.status,
            status_nl=project.status_nl,
            state=project.state.value,
            is_featured=project.is_featured,
            sort_order=project.sort_order,
            published_at=project.published_at.isoformat(),
            created_at=project.created_at.isoformat(),
            updated_at=project.updated_at.isoformat(),
            skill_ids=[str(link.skill_id) for link in ordered_skills],
            skills=[self._map_skill(link.skill) for link in ordered_skills],
            images=[self._map_project_image(image) for image in ordered_images],
        )

    def _map_project_image(self, image: ProjectImage) -> AdminProjectImageOut:
        return AdminProjectImageOut(
            id=str(image.id),
            project_id=str(image.project_id),
            image_file_id=str(image.image_file_id) if image.image_file_id else None,
            alt_text=image.alt_text,
            alt_text_nl=image.alt_text_nl,
            sort_order=image.sort_order,
            is_cover=image.is_cover,
            image=self._map_media(image.image_file, alt=image.alt_text),
        )
