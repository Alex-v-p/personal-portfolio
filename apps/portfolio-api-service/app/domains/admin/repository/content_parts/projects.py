from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Project, ProjectImage, ProjectSkill, ProjectState
from app.domains.admin.schema import AdminProjectOut, AdminProjectUpsertIn


class AdminProjectContentRepository:
    def list_projects(self) -> list[AdminProjectOut]:
        projects = self.session.scalars(
            select(Project)
            .options(
                selectinload(Project.cover_image_file),
                selectinload(Project.images).selectinload(ProjectImage.image_file),
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
            )
            .order_by(Project.sort_order.asc(), Project.published_at.desc(), Project.title.asc())
        ).all()
        return [self._map_project(project) for project in projects]

    def get_project(self, project_id: UUID) -> AdminProjectOut | None:
        project = self.session.scalar(
            select(Project)
            .options(
                selectinload(Project.cover_image_file),
                selectinload(Project.images).selectinload(ProjectImage.image_file),
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
            )
            .where(Project.id == project_id)
        )
        return self._map_project(project) if project else None

    def create_project(self, payload: AdminProjectUpsertIn) -> AdminProjectOut:
        slug_source = payload.slug or payload.title
        project = Project(
            slug=self._ensure_unique_slug(Project, slug_source),
            title=payload.title,
            title_nl=self._normalize_optional_text(payload.title_nl),
            teaser=payload.teaser,
            teaser_nl=self._normalize_optional_text(payload.teaser_nl),
            summary=self._normalize_optional_text(payload.summary),
            summary_nl=self._normalize_optional_text(payload.summary_nl),
            description_markdown=self._normalize_optional_text(payload.description_markdown),
            description_markdown_nl=self._normalize_optional_text(payload.description_markdown_nl),
            cover_image_file_id=self._optional_uuid(payload.cover_image_file_id),
            github_url=self._normalize_optional_text(payload.github_url),
            github_repo_owner=self._normalize_optional_text(payload.github_repo_owner),
            github_repo_name=self._normalize_optional_text(payload.github_repo_name),
            demo_url=self._normalize_optional_text(payload.demo_url),
            company_name=self._normalize_optional_text(payload.company_name),
            started_on=self._parse_date(payload.started_on),
            ended_on=self._parse_date(payload.ended_on),
            duration_label=payload.duration_label,
            duration_label_nl=self._normalize_optional_text(payload.duration_label_nl),
            status=payload.status,
            status_nl=self._normalize_optional_text(payload.status_nl),
            state=ProjectState(payload.state),
            is_featured=payload.is_featured,
            sort_order=payload.sort_order,
            published_at=self._parse_datetime(payload.published_at) or datetime.now(UTC),
        )
        self.session.add(project)
        self.session.flush()
        self._replace_project_skill_links(project, payload.skill_ids)
        self._replace_project_images(project, payload.images)
        self.session.commit()
        return self.get_project(project.id)  # type: ignore[return-value]

    def update_project(self, project_id: UUID, payload: AdminProjectUpsertIn) -> AdminProjectOut | None:
        project = self.session.get(Project, project_id)
        if project is None:
            return None
        slug_source = payload.slug or payload.title
        project.slug = self._ensure_unique_slug(Project, slug_source, current_id=project_id)
        project.title = payload.title
        project.title_nl = self._normalize_optional_text(payload.title_nl)
        project.teaser = payload.teaser
        project.teaser_nl = self._normalize_optional_text(payload.teaser_nl)
        project.summary = self._normalize_optional_text(payload.summary)
        project.summary_nl = self._normalize_optional_text(payload.summary_nl)
        project.description_markdown = self._normalize_optional_text(payload.description_markdown)
        project.description_markdown_nl = self._normalize_optional_text(payload.description_markdown_nl)
        project.cover_image_file_id = self._optional_uuid(payload.cover_image_file_id)
        project.github_url = self._normalize_optional_text(payload.github_url)
        project.github_repo_owner = self._normalize_optional_text(payload.github_repo_owner)
        project.github_repo_name = self._normalize_optional_text(payload.github_repo_name)
        project.demo_url = self._normalize_optional_text(payload.demo_url)
        project.company_name = self._normalize_optional_text(payload.company_name)
        project.started_on = self._parse_date(payload.started_on)
        project.ended_on = self._parse_date(payload.ended_on)
        project.duration_label = payload.duration_label
        project.duration_label_nl = self._normalize_optional_text(payload.duration_label_nl)
        project.status = payload.status
        project.status_nl = self._normalize_optional_text(payload.status_nl)
        project.state = ProjectState(payload.state)
        project.is_featured = payload.is_featured
        project.sort_order = payload.sort_order
        project.published_at = self._parse_datetime(payload.published_at) or project.published_at
        self._replace_project_skill_links(project, payload.skill_ids)
        self._replace_project_images(project, payload.images)
        self.session.commit()
        return self.get_project(project_id)

    def delete_project(self, project_id: UUID) -> bool:
        project = self.session.get(Project, project_id)
        if project is None:
            return False
        self.session.delete(project)
        self.session.commit()
        return True
