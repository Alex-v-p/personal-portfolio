from __future__ import annotations

from sqlalchemy.orm import selectinload

from app.db.models import Project, ProjectImage, ProjectSkill
from app.domains.public_site.schema import ProjectDetailOut, ProjectImageOut, ProjectSummaryOut, SkillSummaryOut


class PublicProjectsRepositoryMixin:
    def list_projects(self) -> list[ProjectSummaryOut]:
        projects = self.session.scalars(
            self._public_project_query()
            .options(
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
                selectinload(Project.cover_image_file),
                selectinload(Project.images).selectinload(ProjectImage.image_file),
            )
            .order_by(Project.sort_order.asc(), Project.title.asc())
        ).all()
        return [self._map_project_summary(project) for project in projects]

    def get_project_by_slug(self, slug: str) -> ProjectDetailOut | None:
        project = self.session.scalar(
            self._public_project_query()
            .options(
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
                selectinload(Project.images).selectinload(ProjectImage.image_file),
                selectinload(Project.cover_image_file),
            )
            .where(Project.slug == slug)
        )
        if project is None:
            return None
        return self._map_project_detail(project)

    def _list_featured_projects(self, limit: int) -> list[ProjectSummaryOut]:
        projects = self.session.scalars(
            self._public_project_query()
            .options(
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
                selectinload(Project.cover_image_file),
                selectinload(Project.images).selectinload(ProjectImage.image_file),
            )
            .order_by(Project.is_featured.desc(), Project.sort_order.asc(), Project.title.asc())
            .limit(limit)
        ).all()
        return [self._map_project_summary(project) for project in projects]

    def _map_project_summary(self, project: Project) -> ProjectSummaryOut:
        ordered_skill_links = sorted(
            [link for link in project.skill_links if link.skill is not None],
            key=lambda item: (item.skill.sort_order, item.skill.name.lower()),
        )
        title = self._localized(project, 'title') or project.title
        teaser = self._localized(project, 'teaser') or project.teaser
        summary = self._localized(project, 'summary') or project.summary
        duration_label = self._localized(project, 'duration_label') or project.duration_label
        status = self._localized(project, 'status') or project.status
        ordered_images = sorted(project.images, key=lambda item: (item.sort_order, str(item.id)))

        return ProjectSummaryOut(
            id=str(project.id),
            slug=project.slug,
            title=title,
            teaser=teaser,
            summary=summary,
            cover_image_file_id=str(project.cover_image_file_id) if project.cover_image_file_id else None,
            cover_image=self._map_media(project.cover_image_file, alt=title),
            github_url=project.github_url,
            github_repo_owner=project.github_repo_owner,
            github_repo_name=project.github_repo_name,
            demo_url=project.demo_url,
            company_name=project.company_name,
            started_on=project.started_on.isoformat() if project.started_on else None,
            ended_on=project.ended_on.isoformat() if project.ended_on else None,
            duration_label=duration_label,
            status=status,
            state=project.state.value,
            is_featured=project.is_featured,
            sort_order=project.sort_order,
            published_at=project.published_at.isoformat(),
            created_at=project.created_at.isoformat(),
            updated_at=project.updated_at.isoformat(),
            skills=[
                SkillSummaryOut(
                    id=str(link.skill.id),
                    category_id=str(link.skill.category_id),
                    name=link.skill.name,
                    years_of_experience=link.skill.years_of_experience,
                    proficiency_label=self._localized_skill_proficiency(link.skill),
                    display_label=self._skill_metric_label(link.skill),
                    icon_key=link.skill.icon_key,
                    sort_order=link.skill.sort_order,
                    is_highlighted=link.skill.is_highlighted,
                )
                for link in ordered_skill_links
            ],
            images=[self._map_project_image(image, title) for image in ordered_images],
        )

    def _map_project_detail(self, project: Project) -> ProjectDetailOut:
        summary = self._map_project_summary(project)
        return ProjectDetailOut(
            **summary.model_dump(),
            description_markdown=self._localized(project, 'description_markdown') or project.description_markdown,
        )

    def _map_project_image(self, image: ProjectImage, fallback_alt: str) -> ProjectImageOut:
        alt_text = self._localized(image, 'alt_text') or image.alt_text
        return ProjectImageOut(
            id=str(image.id),
            project_id=str(image.project_id),
            image_file_id=str(image.image_file_id) if image.image_file_id else None,
            alt_text=alt_text,
            sort_order=image.sort_order,
            is_cover=image.is_cover,
            image=self._map_media(image.image_file, alt=(alt_text or fallback_alt)),
        )
