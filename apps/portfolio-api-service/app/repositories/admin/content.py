from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import (
    BlogPost,
    BlogPostTag,
    Experience,
    NavigationItem,
    Profile,
    Project,
    ProjectImage,
    ProjectSkill,
    PublicationStatus,
    ProjectState,
    SocialLink,
)
from app.schemas.admin import (
    AdminBlogPostOut,
    AdminBlogPostUpsertIn,
    AdminExperienceOut,
    AdminExperienceUpsertIn,
    AdminNavigationItemOut,
    AdminNavigationItemUpsertIn,
    AdminProfileOut,
    AdminProfileUpdateIn,
    AdminProjectOut,
    AdminProjectUpsertIn,
)
from app.repositories.admin.support import AdminRepositorySupport


class AdminContentManagementRepository(AdminRepositorySupport):
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
            title=payload.title.strip(),
            teaser=payload.teaser.strip(),
            summary=self._normalize_optional_text(payload.summary),
            description_markdown=self._normalize_optional_text(payload.description_markdown),
            cover_image_file_id=self._optional_uuid(payload.cover_image_file_id),
            github_url=self._normalize_optional_text(payload.github_url),
            github_repo_owner=self._normalize_optional_text(payload.github_repo_owner),
            github_repo_name=self._normalize_optional_text(payload.github_repo_name),
            demo_url=self._normalize_optional_text(payload.demo_url),
            company_name=self._normalize_optional_text(payload.company_name),
            started_on=self._parse_date(payload.started_on),
            ended_on=self._parse_date(payload.ended_on),
            duration_label=payload.duration_label.strip(),
            status=payload.status.strip(),
            state=ProjectState(payload.state),
            is_featured=payload.is_featured,
            sort_order=payload.sort_order,
            published_at=self._parse_datetime(payload.published_at) or datetime.now(UTC),
        )
        self.session.add(project)
        self.session.flush()
        self._replace_project_skill_links(project, payload.skill_ids)
        self._sync_cover_project_image(project)
        self.session.commit()
        return self.get_project(project.id)  # type: ignore[return-value]

    def update_project(self, project_id: UUID, payload: AdminProjectUpsertIn) -> AdminProjectOut | None:
        project = self.session.get(Project, project_id)
        if project is None:
            return None
        slug_source = payload.slug or payload.title
        project.slug = self._ensure_unique_slug(Project, slug_source, current_id=project_id)
        project.title = payload.title.strip()
        project.teaser = payload.teaser.strip()
        project.summary = self._normalize_optional_text(payload.summary)
        project.description_markdown = self._normalize_optional_text(payload.description_markdown)
        project.cover_image_file_id = self._optional_uuid(payload.cover_image_file_id)
        project.github_url = self._normalize_optional_text(payload.github_url)
        project.github_repo_owner = self._normalize_optional_text(payload.github_repo_owner)
        project.github_repo_name = self._normalize_optional_text(payload.github_repo_name)
        project.demo_url = self._normalize_optional_text(payload.demo_url)
        project.company_name = self._normalize_optional_text(payload.company_name)
        project.started_on = self._parse_date(payload.started_on)
        project.ended_on = self._parse_date(payload.ended_on)
        project.duration_label = payload.duration_label.strip()
        project.status = payload.status.strip()
        project.state = ProjectState(payload.state)
        project.is_featured = payload.is_featured
        project.sort_order = payload.sort_order
        project.published_at = self._parse_datetime(payload.published_at) or project.published_at
        self._replace_project_skill_links(project, payload.skill_ids)
        self._sync_cover_project_image(project)
        self.session.commit()
        return self.get_project(project_id)

    def delete_project(self, project_id: UUID) -> bool:
        project = self.session.get(Project, project_id)
        if project is None:
            return False
        self.session.delete(project)
        self.session.commit()
        return True

    def list_blog_posts(self) -> list[AdminBlogPostOut]:
        posts = self.session.scalars(
            select(BlogPost)
            .options(
                selectinload(BlogPost.cover_image_file),
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
            )
            .order_by(BlogPost.published_at.desc().nullslast(), BlogPost.created_at.desc())
        ).all()
        return [self._map_blog_post(post) for post in posts]

    def get_blog_post(self, post_id: UUID) -> AdminBlogPostOut | None:
        post = self.session.scalar(
            select(BlogPost)
            .options(
                selectinload(BlogPost.cover_image_file),
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
            )
            .where(BlogPost.id == post_id)
        )
        return self._map_blog_post(post) if post else None

    def create_blog_post(self, payload: AdminBlogPostUpsertIn) -> AdminBlogPostOut:
        slug_source = payload.slug or payload.title
        post = BlogPost(
            slug=self._ensure_unique_slug(BlogPost, slug_source),
            title=payload.title.strip(),
            excerpt=payload.excerpt.strip(),
            content_markdown=payload.content_markdown,
            cover_image_file_id=self._optional_uuid(payload.cover_image_file_id),
            cover_image_alt=self._normalize_optional_text(payload.cover_image_alt),
            reading_time_minutes=payload.reading_time_minutes,
            status=PublicationStatus(payload.status),
            is_featured=payload.is_featured,
            seo_title=self._normalize_optional_text(payload.seo_title),
            seo_description=self._normalize_optional_text(payload.seo_description),
            published_at=self._parse_datetime(payload.published_at),
        )
        self.session.add(post)
        self.session.flush()
        self._replace_blog_post_tags(post, payload.tag_ids)
        self.session.commit()
        return self.get_blog_post(post.id)  # type: ignore[return-value]

    def update_blog_post(self, post_id: UUID, payload: AdminBlogPostUpsertIn) -> AdminBlogPostOut | None:
        post = self.session.get(BlogPost, post_id)
        if post is None:
            return None
        slug_source = payload.slug or payload.title
        post.slug = self._ensure_unique_slug(BlogPost, slug_source, current_id=post_id)
        post.title = payload.title.strip()
        post.excerpt = payload.excerpt.strip()
        post.content_markdown = payload.content_markdown
        post.cover_image_file_id = self._optional_uuid(payload.cover_image_file_id)
        post.cover_image_alt = self._normalize_optional_text(payload.cover_image_alt)
        post.reading_time_minutes = payload.reading_time_minutes
        post.status = PublicationStatus(payload.status)
        post.is_featured = payload.is_featured
        post.seo_title = self._normalize_optional_text(payload.seo_title)
        post.seo_description = self._normalize_optional_text(payload.seo_description)
        post.published_at = self._parse_datetime(payload.published_at)
        self._replace_blog_post_tags(post, payload.tag_ids)
        self.session.commit()
        return self.get_blog_post(post_id)

    def delete_blog_post(self, post_id: UUID) -> bool:
        post = self.session.get(BlogPost, post_id)
        if post is None:
            return False
        self.session.delete(post)
        self.session.commit()
        return True

    def list_experiences(self) -> list[AdminExperienceOut]:
        experiences = self.session.scalars(
            select(Experience)
            .options(
                selectinload(Experience.logo_file),
                selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill),
            )
            .order_by(Experience.sort_order.asc(), Experience.start_date.desc(), Experience.organization_name.asc())
        ).all()
        return [self._map_experience(experience) for experience in experiences]

    def get_experience(self, experience_id: UUID) -> AdminExperienceOut | None:
        experience = self.session.scalar(
            select(Experience)
            .options(
                selectinload(Experience.logo_file),
                selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill),
            )
            .where(Experience.id == experience_id)
        )
        return self._map_experience(experience) if experience else None

    def create_experience(self, payload: AdminExperienceUpsertIn) -> AdminExperienceOut:
        experience = Experience(
            organization_name=payload.organization_name.strip(),
            role_title=payload.role_title.strip(),
            location=self._normalize_optional_text(payload.location),
            experience_type=payload.experience_type.strip(),
            start_date=self._parse_date(payload.start_date) or date.today(),
            end_date=self._parse_date(payload.end_date),
            is_current=payload.is_current,
            summary=payload.summary.strip(),
            description_markdown=self._normalize_optional_text(payload.description_markdown),
            logo_file_id=self._optional_uuid(payload.logo_file_id),
            sort_order=payload.sort_order,
        )
        self.session.add(experience)
        self.session.flush()
        self._replace_experience_skill_links(experience, payload.skill_ids)
        self.session.commit()
        return self.get_experience(experience.id)  # type: ignore[return-value]

    def update_experience(self, experience_id: UUID, payload: AdminExperienceUpsertIn) -> AdminExperienceOut | None:
        experience = self.session.get(Experience, experience_id)
        if experience is None:
            return None
        experience.organization_name = payload.organization_name.strip()
        experience.role_title = payload.role_title.strip()
        experience.location = self._normalize_optional_text(payload.location)
        experience.experience_type = payload.experience_type.strip()
        experience.start_date = self._parse_date(payload.start_date) or experience.start_date
        experience.end_date = self._parse_date(payload.end_date)
        experience.is_current = payload.is_current
        experience.summary = payload.summary.strip()
        experience.description_markdown = self._normalize_optional_text(payload.description_markdown)
        experience.logo_file_id = self._optional_uuid(payload.logo_file_id)
        experience.sort_order = payload.sort_order
        self._replace_experience_skill_links(experience, payload.skill_ids)
        self.session.commit()
        return self.get_experience(experience_id)

    def delete_experience(self, experience_id: UUID) -> bool:
        experience = self.session.get(Experience, experience_id)
        if experience is None:
            return False
        self.session.delete(experience)
        self.session.commit()
        return True

    def list_navigation_items(self) -> list[AdminNavigationItemOut]:
        items = self.session.scalars(select(NavigationItem).order_by(NavigationItem.sort_order.asc(), NavigationItem.label.asc())).all()
        return [self._map_navigation_item(item) for item in items]

    def create_navigation_item(self, payload: AdminNavigationItemUpsertIn) -> AdminNavigationItemOut:
        item = NavigationItem(
            label=payload.label.strip(),
            route_path=payload.route_path.strip(),
            is_external=payload.is_external,
            sort_order=payload.sort_order,
            is_visible=payload.is_visible,
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return self._map_navigation_item(item)

    def update_navigation_item(self, item_id: UUID, payload: AdminNavigationItemUpsertIn) -> AdminNavigationItemOut | None:
        item = self.session.get(NavigationItem, item_id)
        if item is None:
            return None
        item.label = payload.label.strip()
        item.route_path = payload.route_path.strip()
        item.is_external = payload.is_external
        item.sort_order = payload.sort_order
        item.is_visible = payload.is_visible
        self.session.commit()
        self.session.refresh(item)
        return self._map_navigation_item(item)

    def delete_navigation_item(self, item_id: UUID) -> bool:
        item = self.session.get(NavigationItem, item_id)
        if item is None:
            return False
        self.session.delete(item)
        self.session.commit()
        return True

    def get_profile(self) -> AdminProfileOut | None:
        profile = self.session.scalar(
            select(Profile)
            .options(
                selectinload(Profile.avatar_file),
                selectinload(Profile.hero_image_file),
                selectinload(Profile.resume_file),
                selectinload(Profile.social_links),
            )
            .order_by(Profile.updated_at.desc())
        )
        return self._map_profile(profile) if profile else None

    def update_profile(self, payload: AdminProfileUpdateIn) -> AdminProfileOut | None:
        profile = self.session.scalar(
            select(Profile)
            .options(selectinload(Profile.social_links))
            .order_by(Profile.updated_at.desc())
        )
        if profile is None:
            return None

        profile.first_name = payload.first_name.strip()
        profile.last_name = payload.last_name.strip()
        profile.headline = payload.headline.strip()
        profile.short_intro = payload.short_intro.strip()
        profile.long_bio = self._normalize_optional_text(payload.long_bio)
        profile.location = self._normalize_optional_text(payload.location)
        profile.email = str(payload.email).strip() if payload.email else None
        profile.phone = self._normalize_optional_text(payload.phone)
        profile.avatar_file_id = self._optional_uuid(payload.avatar_file_id)
        profile.hero_image_file_id = self._optional_uuid(payload.hero_image_file_id)
        profile.resume_file_id = self._optional_uuid(payload.resume_file_id)
        profile.cta_primary_label = self._normalize_optional_text(payload.cta_primary_label)
        profile.cta_primary_url = self._normalize_optional_text(payload.cta_primary_url)
        profile.cta_secondary_label = self._normalize_optional_text(payload.cta_secondary_label)
        profile.cta_secondary_url = self._normalize_optional_text(payload.cta_secondary_url)
        profile.is_public = payload.is_public

        profile.social_links.clear()
        for index, link in enumerate(payload.social_links):
            profile.social_links.append(
                SocialLink(
                    id=self._optional_uuid(link.id),
                    platform=link.platform.strip().lower(),
                    label=link.label.strip(),
                    url=link.url.strip(),
                    icon_key=self._normalize_optional_text(link.icon_key),
                    sort_order=link.sort_order if link.sort_order is not None else index,
                    is_visible=link.is_visible,
                )
            )

        self.session.commit()
        return self.get_profile()
