from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
import re
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.db.models import (
    AdminUser,
    AssistantConversation,
    AssistantRole,
    BlogPost,
    BlogPostTag,
    BlogTag,
    ContactMessage,
    EventType,
    Experience,
    ExperienceSkill,
    GithubContributionDay,
    GithubSnapshot,
    MediaFile,
    MediaVisibility,
    NavigationItem,
    Profile,
    Project,
    SiteEvent,
    ProjectImage,
    ProjectSkill,
    ProjectState,
    PublicationStatus,
    Skill,
    SkillCategory,
    SocialLink,
)
from app.schemas.admin import (
    AdminAssistantConversationSummaryOut,
    AdminBlogPostOut,
    AdminBlogPostUpsertIn,
    AdminBlogTagOut,
    AdminBlogTagUpsertIn,
    AdminContactMessageOut,
    AdminDashboardSummaryOut,
    AdminSiteActivityOut,
    AdminSiteActivitySummaryOut,
    AdminSiteEventOut,
    AdminVisitSessionSummaryOut,
    AdminVisitorActivitySummaryOut,
    AdminExperienceOut,
    AdminExperienceUpsertIn,
    AdminGithubContributionDayOut,
    AdminGithubSnapshotOut,
    AdminGithubSnapshotUpsertIn,
    AdminMediaFileOut,
    AdminNavigationItemOut,
    AdminNavigationItemUpsertIn,
    AdminProfileOut,
    AdminProfileUpdateIn,
    AdminProjectOut,
    AdminProjectUpsertIn,
    AdminReferenceDataOut,
    AdminSkillCategoryOut,
    AdminSkillCategoryUpsertIn,
    AdminSkillOut,
    AdminSkillUpsertIn,
    AdminSocialLinkOut,
    AdminUserCreateIn,
    AdminUserOut,
    AdminUserUpdateIn,
)
from app.schemas.public import PublicMediaAssetOut, SkillSummaryOut
from app.services.github_stats_sync import SyncedGithubSnapshot
from app.services.media_resolver import PublicMediaUrlResolver
from app.services.media_storage import StoredMediaObject
from app.services.security import hash_password

_slug_cleanup_pattern = re.compile(r'[^a-z0-9]+')


class AdminContentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.media_resolver = PublicMediaUrlResolver()

    def get_admin_user_by_email(self, email: str) -> AdminUser | None:
        return self.session.scalar(select(AdminUser).where(func.lower(AdminUser.email) == email.strip().lower()))

    def map_admin_user(self, admin_user: AdminUser) -> AdminUserOut:
        return AdminUserOut(
            id=str(admin_user.id),
            email=admin_user.email,
            display_name=admin_user.display_name,
            is_active=admin_user.is_active,
            created_at=admin_user.created_at.isoformat(),
        )

    def list_admin_users(self) -> list[AdminUserOut]:
        users = self.session.scalars(select(AdminUser).order_by(AdminUser.created_at.desc(), AdminUser.email.asc())).all()
        return [self.map_admin_user(user) for user in users]

    def create_admin_user(self, payload: AdminUserCreateIn) -> AdminUserOut:
        user = AdminUser(
            email=str(payload.email).strip().lower(),
            display_name=payload.display_name.strip(),
            password_hash=hash_password(payload.password),
            is_active=payload.is_active,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return self.map_admin_user(user)

    def update_admin_user(self, admin_user_id: UUID, payload: AdminUserUpdateIn) -> AdminUserOut | None:
        user = self.session.get(AdminUser, admin_user_id)
        if user is None:
            return None
        user.email = str(payload.email).strip().lower()
        user.display_name = payload.display_name.strip()
        user.is_active = payload.is_active
        if payload.password:
            user.password_hash = hash_password(payload.password)
        self.session.commit()
        self.session.refresh(user)
        return self.map_admin_user(user)

    def delete_admin_user(self, admin_user_id: UUID) -> bool:
        user = self.session.get(AdminUser, admin_user_id)
        if user is None:
            return False
        self.session.delete(user)
        self.session.commit()
        return True

    def get_dashboard_summary(self) -> AdminDashboardSummaryOut:
        return AdminDashboardSummaryOut(
            projects=self.session.scalar(select(func.count(Project.id))) or 0,
            blog_posts=self.session.scalar(select(func.count(BlogPost.id))) or 0,
            unread_messages=self.session.scalar(select(func.count(ContactMessage.id)).where(ContactMessage.is_read.is_(False))) or 0,
            skills=self.session.scalar(select(func.count(Skill.id))) or 0,
            skill_categories=self.session.scalar(select(func.count(SkillCategory.id))) or 0,
            media_files=self.session.scalar(select(func.count(MediaFile.id))) or 0,
            experiences=self.session.scalar(select(func.count(Experience.id))) or 0,
            navigation_items=self.session.scalar(select(func.count(NavigationItem.id))) or 0,
            blog_tags=self.session.scalar(select(func.count(BlogTag.id))) or 0,
            admin_users=self.session.scalar(select(func.count(AdminUser.id))) or 0,
            github_snapshots=self.session.scalar(select(func.count(GithubSnapshot.id))) or 0,
        )

    def get_reference_data(self) -> AdminReferenceDataOut:
        skills = self.list_skills()
        skill_categories = self.list_skill_categories()
        media_files = self.list_media_files()
        blog_tags = self.list_blog_tags()
        return AdminReferenceDataOut(
            skills=skills,
            skill_categories=skill_categories,
            media_files=media_files,
            blog_tags=blog_tags,
            project_states=[state.value for state in ProjectState],
            publication_statuses=[status.value for status in PublicationStatus],
        )

    def list_media_files(self) -> list[AdminMediaFileOut]:
        media_files = self.session.scalars(select(MediaFile).order_by(MediaFile.created_at.desc())).all()
        return [self._map_media_file(media_file) for media_file in media_files]

    def create_media_file(
        self,
        *,
        stored_object: StoredMediaObject,
        uploaded_by_id: UUID,
        title: str | None,
        alt_text: str | None,
        description: str | None,
        visibility: str,
    ) -> AdminMediaFileOut:
        media_file = MediaFile(
            bucket_name=stored_object.bucket_name,
            object_key=stored_object.object_key,
            original_filename=stored_object.original_filename,
            stored_filename=stored_object.stored_filename,
            mime_type=stored_object.mime_type,
            file_size_bytes=stored_object.file_size_bytes,
            checksum=stored_object.checksum,
            public_url=None,
            alt_text=self._normalize_optional_text(alt_text),
            title=self._normalize_optional_text(title),
            description=self._normalize_optional_text(description),
            visibility=MediaVisibility(visibility),
            uploaded_by_id=uploaded_by_id,
        )
        self.session.add(media_file)
        self.session.commit()
        self.session.refresh(media_file)
        return self._map_media_file(media_file)

    def get_media_file(self, media_id: UUID) -> MediaFile | None:
        return self.session.get(MediaFile, media_id)

    def delete_media_file(self, media_id: UUID) -> bool:
        media_file = self.session.get(MediaFile, media_id)
        if media_file is None:
            return False
        self.session.delete(media_file)
        self.session.commit()
        return True

    def list_skill_categories(self) -> list[AdminSkillCategoryOut]:
        categories = self.session.scalars(select(SkillCategory).order_by(SkillCategory.sort_order.asc(), SkillCategory.name.asc())).all()
        return [self._map_skill_category(category) for category in categories]

    def create_skill_category(self, payload: AdminSkillCategoryUpsertIn) -> AdminSkillCategoryOut:
        category = SkillCategory(name=payload.name.strip(), description=self._normalize_optional_text(payload.description), sort_order=payload.sort_order)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return self._map_skill_category(category)

    def update_skill_category(self, category_id: UUID, payload: AdminSkillCategoryUpsertIn) -> AdminSkillCategoryOut | None:
        category = self.session.get(SkillCategory, category_id)
        if category is None:
            return None
        category.name = payload.name.strip()
        category.description = self._normalize_optional_text(payload.description)
        category.sort_order = payload.sort_order
        self.session.commit()
        self.session.refresh(category)
        return self._map_skill_category(category)

    def delete_skill_category(self, category_id: UUID) -> tuple[bool, str | None]:
        category = self.session.get(SkillCategory, category_id)
        if category is None:
            return False, 'not_found'
        in_use = self.session.scalar(select(func.count(Skill.id)).where(Skill.category_id == category_id)) or 0
        if in_use:
            return False, 'in_use'
        self.session.delete(category)
        self.session.commit()
        return True, None

    def list_skills(self) -> list[AdminSkillOut]:
        skills = self.session.scalars(select(Skill).order_by(Skill.sort_order.asc(), Skill.name.asc())).all()
        return [self._map_admin_skill(skill) for skill in skills]

    def create_skill(self, payload: AdminSkillUpsertIn) -> AdminSkillOut:
        skill = Skill(
            category_id=self._required_uuid(payload.category_id),
            name=payload.name.strip(),
            years_of_experience=payload.years_of_experience,
            icon_key=self._normalize_optional_text(payload.icon_key),
            sort_order=payload.sort_order,
            is_highlighted=payload.is_highlighted,
        )
        self.session.add(skill)
        self.session.commit()
        self.session.refresh(skill)
        return self._map_admin_skill(skill)

    def update_skill(self, skill_id: UUID, payload: AdminSkillUpsertIn) -> AdminSkillOut | None:
        skill = self.session.get(Skill, skill_id)
        if skill is None:
            return None
        skill.category_id = self._required_uuid(payload.category_id)
        skill.name = payload.name.strip()
        skill.years_of_experience = payload.years_of_experience
        skill.icon_key = self._normalize_optional_text(payload.icon_key)
        skill.sort_order = payload.sort_order
        skill.is_highlighted = payload.is_highlighted
        self.session.commit()
        self.session.refresh(skill)
        return self._map_admin_skill(skill)

    def delete_skill(self, skill_id: UUID) -> bool:
        skill = self.session.get(Skill, skill_id)
        if skill is None:
            return False
        self.session.delete(skill)
        self.session.commit()
        return True

    def list_blog_tags(self) -> list[AdminBlogTagOut]:
        tags = self.session.scalars(select(BlogTag).order_by(BlogTag.name.asc())).all()
        return [AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug) for tag in tags]

    def create_blog_tag(self, payload: AdminBlogTagUpsertIn) -> AdminBlogTagOut:
        name = payload.name.strip()
        tag = BlogTag(name=name, slug=self._ensure_unique_slug(BlogTag, payload.slug or name))
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug)

    def update_blog_tag(self, tag_id: UUID, payload: AdminBlogTagUpsertIn) -> AdminBlogTagOut | None:
        tag = self.session.get(BlogTag, tag_id)
        if tag is None:
            return None
        name = payload.name.strip()
        tag.name = name
        tag.slug = self._ensure_unique_slug(BlogTag, payload.slug or name, current_id=tag_id)
        self.session.commit()
        self.session.refresh(tag)
        return AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug)

    def delete_blog_tag(self, tag_id: UUID) -> bool:
        tag = self.session.get(BlogTag, tag_id)
        if tag is None:
            return False
        self.session.delete(tag)
        self.session.commit()
        return True

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

    def list_github_snapshots(self) -> list[AdminGithubSnapshotOut]:
        snapshots = self.session.scalars(
            select(GithubSnapshot)
            .options(selectinload(GithubSnapshot.contribution_days))
            .order_by(GithubSnapshot.snapshot_date.desc(), GithubSnapshot.created_at.desc())
        ).all()
        return [self._map_github_snapshot(snapshot) for snapshot in snapshots]

    def get_github_snapshot(self, snapshot_id: UUID) -> AdminGithubSnapshotOut | None:
        snapshot = self.session.scalar(
            select(GithubSnapshot)
            .options(selectinload(GithubSnapshot.contribution_days))
            .where(GithubSnapshot.id == snapshot_id)
        )
        return self._map_github_snapshot(snapshot) if snapshot else None

    def create_github_snapshot(self, payload: AdminGithubSnapshotUpsertIn) -> AdminGithubSnapshotOut:
        snapshot = GithubSnapshot(
            snapshot_date=self._parse_date(payload.snapshot_date) or date.today(),
            username=payload.username.strip(),
            public_repo_count=payload.public_repo_count,
            followers_count=payload.followers_count,
            following_count=payload.following_count,
            total_stars=payload.total_stars,
            total_commits=payload.total_commits,
            raw_payload=payload.raw_payload,
        )
        self.session.add(snapshot)
        self.session.flush()
        self._replace_github_contribution_days(snapshot, payload)
        self.session.commit()
        return self.get_github_snapshot(snapshot.id)  # type: ignore[return-value]

    def update_github_snapshot(self, snapshot_id: UUID, payload: AdminGithubSnapshotUpsertIn) -> AdminGithubSnapshotOut | None:
        snapshot = self.session.get(GithubSnapshot, snapshot_id)
        if snapshot is None:
            return None
        snapshot.snapshot_date = self._parse_date(payload.snapshot_date) or snapshot.snapshot_date
        snapshot.username = payload.username.strip()
        snapshot.public_repo_count = payload.public_repo_count
        snapshot.followers_count = payload.followers_count
        snapshot.following_count = payload.following_count
        snapshot.total_stars = payload.total_stars
        snapshot.total_commits = payload.total_commits
        snapshot.raw_payload = payload.raw_payload
        self._replace_github_contribution_days(snapshot, payload)
        self.session.commit()
        return self.get_github_snapshot(snapshot_id)

    def delete_github_snapshot(self, snapshot_id: UUID) -> bool:
        snapshot = self.session.get(GithubSnapshot, snapshot_id)
        if snapshot is None:
            return False
        self.session.delete(snapshot)
        self.session.commit()
        return True

    def refresh_github_snapshot(self, synced_snapshot: SyncedGithubSnapshot, *, prune_history: bool = True) -> AdminGithubSnapshotOut:
        latest_snapshot = self.session.scalar(
            select(GithubSnapshot)
            .options(selectinload(GithubSnapshot.contribution_days))
            .where(func.lower(GithubSnapshot.username) == synced_snapshot.username.strip().lower())
            .order_by(GithubSnapshot.snapshot_date.desc(), GithubSnapshot.created_at.desc())
        )

        if latest_snapshot is None:
            latest_snapshot = GithubSnapshot(
                snapshot_date=self._parse_date(synced_snapshot.snapshot_date) or date.today(),
                username=synced_snapshot.username.strip(),
                public_repo_count=synced_snapshot.public_repo_count,
                followers_count=synced_snapshot.followers_count,
                following_count=synced_snapshot.following_count,
                total_stars=synced_snapshot.total_stars,
                total_commits=synced_snapshot.total_commits,
                raw_payload=synced_snapshot.raw_payload,
            )
            self.session.add(latest_snapshot)
            self.session.flush()
        else:
            latest_snapshot.snapshot_date = self._parse_date(synced_snapshot.snapshot_date) or latest_snapshot.snapshot_date
            latest_snapshot.username = synced_snapshot.username.strip()
            latest_snapshot.public_repo_count = synced_snapshot.public_repo_count
            latest_snapshot.followers_count = synced_snapshot.followers_count
            latest_snapshot.following_count = synced_snapshot.following_count
            latest_snapshot.total_stars = synced_snapshot.total_stars
            latest_snapshot.total_commits = synced_snapshot.total_commits
            latest_snapshot.raw_payload = synced_snapshot.raw_payload

        latest_snapshot.contribution_days.clear()
        self.session.flush()
        for day in synced_snapshot.contribution_days:
            latest_snapshot.contribution_days.append(
                GithubContributionDay(
                    contribution_date=self._parse_date(day.date) or date.today(),
                    contribution_count=day.count,
                    level=day.level,
                )
            )
        self.session.flush()

        if prune_history:
            obsolete_snapshots = self.session.scalars(
                select(GithubSnapshot).where(
                    func.lower(GithubSnapshot.username) == synced_snapshot.username.strip().lower(),
                    GithubSnapshot.id != latest_snapshot.id,
                )
            ).all()
            for snapshot in obsolete_snapshots:
                self.session.delete(snapshot)

        self.session.commit()
        return self.get_github_snapshot(latest_snapshot.id)  # type: ignore[return-value]

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

    def list_contact_messages(self) -> list[AdminContactMessageOut]:
        messages = self.session.scalars(select(ContactMessage).order_by(ContactMessage.created_at.desc())).all()
        return [self._map_contact_message(message) for message in messages]

    def get_site_activity(self) -> AdminSiteActivityOut:
        events = self.session.scalars(
            select(SiteEvent).order_by(SiteEvent.created_at.desc())
        ).all()
        conversations = self.session.scalars(
            select(AssistantConversation)
            .options(selectinload(AssistantConversation.messages))
            .order_by(AssistantConversation.last_message_at.desc())
        ).all()

        visitors, visits = self._build_site_activity_rollups(events)
        conversation_links = self._build_conversation_activity_links(events)

        return AdminSiteActivityOut(
            summary=AdminSiteActivitySummaryOut(
                total_events=len(events),
                unique_visitors=len({event.visitor_id for event in events if event.visitor_id}),
                page_views=sum(1 for event in events if event.event_type == EventType.PAGE_VIEW),
                assistant_messages=sum(1 for event in events if event.event_type == EventType.ASSISTANT_MESSAGE),
                contact_submissions=sum(1 for event in events if event.event_type == EventType.CONTACT_SUBMIT),
            ),
            visitors=visitors,
            visits=visits,
            events=[self._map_site_event(item) for item in events],
            assistant_conversations=[
                self._map_assistant_conversation(item, conversation_links.get(str(item.id))) for item in conversations
            ],
        )

    def update_contact_message_status(self, message_id: UUID, *, is_read: bool) -> AdminContactMessageOut | None:
        message = self.session.get(ContactMessage, message_id)
        if message is None:
            return None
        message.is_read = is_read
        self.session.commit()
        self.session.refresh(message)
        return self._map_contact_message(message)

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

    def _map_profile(self, profile: Profile) -> AdminProfileOut:
        return AdminProfileOut(
            id=str(profile.id),
            first_name=profile.first_name,
            last_name=profile.last_name,
            headline=profile.headline,
            short_intro=profile.short_intro,
            long_bio=profile.long_bio,
            location=profile.location,
            email=profile.email,
            phone=profile.phone,
            avatar_file_id=str(profile.avatar_file_id) if profile.avatar_file_id else None,
            hero_image_file_id=str(profile.hero_image_file_id) if profile.hero_image_file_id else None,
            resume_file_id=str(profile.resume_file_id) if profile.resume_file_id else None,
            avatar=self._map_media(profile.avatar_file, alt=f'{profile.first_name} {profile.last_name} avatar'),
            hero_image=self._map_media(profile.hero_image_file, alt=f'{profile.first_name} {profile.last_name} hero image'),
            resume=self._map_media(profile.resume_file, alt=f'{profile.first_name} {profile.last_name} resume'),
            cta_primary_label=profile.cta_primary_label,
            cta_primary_url=profile.cta_primary_url,
            cta_secondary_label=profile.cta_secondary_label,
            cta_secondary_url=profile.cta_secondary_url,
            is_public=profile.is_public,
            social_links=[
                AdminSocialLinkOut(
                    id=str(link.id),
                    platform=link.platform,
                    label=link.label,
                    url=link.url,
                    icon_key=link.icon_key,
                    sort_order=link.sort_order,
                    is_visible=link.is_visible,
                )
                for link in sorted(profile.social_links, key=lambda item: (item.sort_order, item.label.lower()))
            ],
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat(),
        )

    def _map_skill_category(self, category: SkillCategory) -> AdminSkillCategoryOut:
        return AdminSkillCategoryOut(
            id=str(category.id),
            name=category.name,
            description=category.description,
            sort_order=category.sort_order,
        )

    def _map_admin_skill(self, skill: Skill) -> AdminSkillOut:
        return AdminSkillOut(
            id=str(skill.id),
            category_id=str(skill.category_id),
            name=skill.name,
            years_of_experience=skill.years_of_experience,
            icon_key=skill.icon_key,
            sort_order=skill.sort_order,
            is_highlighted=skill.is_highlighted,
        )

    def _map_project(self, project: Project) -> AdminProjectOut:
        ordered_skills = sorted(project.skill_links, key=lambda link: (link.skill.sort_order, link.skill.name.lower()))
        return AdminProjectOut(
            id=str(project.id),
            slug=project.slug,
            title=project.title,
            teaser=project.teaser,
            summary=project.summary,
            description_markdown=project.description_markdown,
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
            status=project.status,
            state=project.state.value,
            is_featured=project.is_featured,
            sort_order=project.sort_order,
            published_at=project.published_at.isoformat(),
            created_at=project.created_at.isoformat(),
            updated_at=project.updated_at.isoformat(),
            skill_ids=[str(link.skill_id) for link in ordered_skills],
            skills=[self._map_skill(link.skill) for link in ordered_skills],
        )

    def _map_blog_post(self, post: BlogPost) -> AdminBlogPostOut:
        ordered_tags = sorted((link.tag for link in post.tag_links), key=lambda tag: tag.name.lower())
        return AdminBlogPostOut(
            id=str(post.id),
            slug=post.slug,
            title=post.title,
            excerpt=post.excerpt,
            content_markdown=post.content_markdown,
            cover_image_file_id=str(post.cover_image_file_id) if post.cover_image_file_id else None,
            cover_image_alt=post.cover_image_alt,
            cover_image=self._map_media(post.cover_image_file, alt=post.cover_image_alt or f'{post.title} cover image'),
            reading_time_minutes=post.reading_time_minutes,
            status=post.status.value,
            is_featured=post.is_featured,
            published_at=post.published_at.isoformat() if post.published_at else None,
            seo_title=post.seo_title,
            seo_description=post.seo_description,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            tag_ids=[str(tag.id) for tag in ordered_tags],
            tag_names=[tag.name for tag in ordered_tags],
            tags=[AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug) for tag in ordered_tags],
        )

    def _map_experience(self, experience: Experience) -> AdminExperienceOut:
        ordered_skills = sorted(experience.skill_links, key=lambda link: (link.skill.sort_order, link.skill.name.lower()))
        return AdminExperienceOut(
            id=str(experience.id),
            organization_name=experience.organization_name,
            role_title=experience.role_title,
            location=experience.location,
            experience_type=experience.experience_type,
            start_date=experience.start_date.isoformat(),
            end_date=experience.end_date.isoformat() if experience.end_date else None,
            is_current=experience.is_current,
            summary=experience.summary,
            description_markdown=experience.description_markdown,
            logo_file_id=str(experience.logo_file_id) if experience.logo_file_id else None,
            logo=self._map_media(experience.logo_file, alt=f'{experience.organization_name} logo'),
            sort_order=experience.sort_order,
            created_at=experience.created_at.isoformat(),
            updated_at=experience.updated_at.isoformat(),
            skill_ids=[str(link.skill_id) for link in ordered_skills],
            skills=[self._map_skill(link.skill) for link in ordered_skills],
        )

    def _map_navigation_item(self, item: NavigationItem) -> AdminNavigationItemOut:
        return AdminNavigationItemOut(
            id=str(item.id),
            label=item.label,
            route_path=item.route_path,
            is_external=item.is_external,
            sort_order=item.sort_order,
            is_visible=item.is_visible,
        )

    def _map_github_snapshot(self, snapshot: GithubSnapshot) -> AdminGithubSnapshotOut:
        ordered_days = sorted(snapshot.contribution_days, key=lambda day: day.contribution_date)
        return AdminGithubSnapshotOut(
            id=str(snapshot.id),
            snapshot_date=snapshot.snapshot_date.isoformat(),
            username=snapshot.username,
            public_repo_count=snapshot.public_repo_count,
            followers_count=snapshot.followers_count,
            following_count=snapshot.following_count,
            total_stars=snapshot.total_stars,
            total_commits=snapshot.total_commits,
            raw_payload=snapshot.raw_payload,
            contribution_days=[
                AdminGithubContributionDayOut(
                    date=day.contribution_date.isoformat(),
                    count=day.contribution_count,
                    level=day.level,
                )
                for day in ordered_days
            ],
            created_at=snapshot.created_at.isoformat(),
            updated_at=snapshot.created_at.isoformat(),
        )

    def _map_contact_message(self, message: ContactMessage) -> AdminContactMessageOut:
        return AdminContactMessageOut(
            id=str(message.id),
            name=message.name,
            email=message.email,
            subject=message.subject,
            message=message.message,
            source_page=message.source_page,
            is_read=message.is_read,
            created_at=message.created_at.isoformat(),
            updated_at=message.updated_at.isoformat(),
        )

    def _map_site_event(self, event: SiteEvent) -> AdminSiteEventOut:
        metadata = event.metadata_json or None
        ip_address = None
        if isinstance(metadata, dict):
            ip_value = metadata.get('ip_address')
            if isinstance(ip_value, str):
                ip_address = ip_value
        return AdminSiteEventOut(
            id=str(event.id),
            event_type=event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            page_path=event.page_path,
            visitor_id=event.visitor_id,
            session_id=event.session_id,
            referrer=event.referrer,
            user_agent=event.user_agent,
            ip_address=ip_address,
            metadata=metadata,
            created_at=event.created_at.isoformat(),
        )

    def _build_site_activity_rollups(
        self, events: list[SiteEvent]
    ) -> tuple[list[AdminVisitorActivitySummaryOut], list[AdminVisitSessionSummaryOut]]:
        visitor_rollups: dict[str, dict[str, Any]] = {}
        visit_rollups: dict[tuple[str, str], dict[str, Any]] = {}

        for event in reversed(events):
            metadata = event.metadata_json if isinstance(event.metadata_json, dict) else {}
            ip_address = metadata.get('ip_address') if isinstance(metadata.get('ip_address'), str) else None

            visitor_entry = visitor_rollups.setdefault(
                event.visitor_id,
                {
                    'visitor_id': event.visitor_id,
                    'first_seen_at': event.created_at,
                    'last_seen_at': event.created_at,
                    'total_events': 0,
                    'page_views': 0,
                    'assistant_messages': 0,
                    'contact_submissions': 0,
                    'session_ids': set(),
                    'latest_page_path': None,
                    'latest_ip_address': None,
                },
            )
            visitor_entry['first_seen_at'] = min(visitor_entry['first_seen_at'], event.created_at)
            visitor_entry['last_seen_at'] = max(visitor_entry['last_seen_at'], event.created_at)
            visitor_entry['total_events'] += 1
            if event.session_id:
                visitor_entry['session_ids'].add(event.session_id)
            if event.event_type == EventType.PAGE_VIEW:
                visitor_entry['page_views'] += 1
            elif event.event_type == EventType.ASSISTANT_MESSAGE:
                visitor_entry['assistant_messages'] += 1
            elif event.event_type == EventType.CONTACT_SUBMIT:
                visitor_entry['contact_submissions'] += 1
            if visitor_entry['last_seen_at'] == event.created_at:
                visitor_entry['latest_page_path'] = event.page_path
                visitor_entry['latest_ip_address'] = ip_address

            if event.session_id:
                visit_key = (event.visitor_id, event.session_id)
                visit_entry = visit_rollups.setdefault(
                    visit_key,
                    {
                        'session_id': event.session_id,
                        'visitor_id': event.visitor_id,
                        'started_at': event.created_at,
                        'last_activity_at': event.created_at,
                        'total_events': 0,
                        'page_views': 0,
                        'assistant_messages': 0,
                        'contact_submissions': 0,
                        'entry_page_path': event.page_path,
                        'last_page_path': event.page_path,
                        'ip_address': ip_address,
                    },
                )
                visit_entry['started_at'] = min(visit_entry['started_at'], event.created_at)
                visit_entry['last_activity_at'] = max(visit_entry['last_activity_at'], event.created_at)
                visit_entry['total_events'] += 1
                if event.event_type == EventType.PAGE_VIEW:
                    visit_entry['page_views'] += 1
                elif event.event_type == EventType.ASSISTANT_MESSAGE:
                    visit_entry['assistant_messages'] += 1
                elif event.event_type == EventType.CONTACT_SUBMIT:
                    visit_entry['contact_submissions'] += 1
                if event.created_at <= visit_entry['started_at']:
                    visit_entry['entry_page_path'] = event.page_path
                if event.created_at >= visit_entry['last_activity_at']:
                    visit_entry['last_page_path'] = event.page_path
                    if ip_address:
                        visit_entry['ip_address'] = ip_address

        visitors = [
            AdminVisitorActivitySummaryOut(
                visitor_id=item['visitor_id'],
                first_seen_at=item['first_seen_at'].isoformat(),
                last_seen_at=item['last_seen_at'].isoformat(),
                total_events=item['total_events'],
                unique_sessions=len(item['session_ids']),
                page_views=item['page_views'],
                assistant_messages=item['assistant_messages'],
                contact_submissions=item['contact_submissions'],
                latest_page_path=item['latest_page_path'],
                latest_ip_address=item['latest_ip_address'],
            )
            for item in sorted(visitor_rollups.values(), key=lambda value: value['last_seen_at'], reverse=True)
        ]
        visits = [
            AdminVisitSessionSummaryOut(
                session_id=item['session_id'],
                visitor_id=item['visitor_id'],
                started_at=item['started_at'].isoformat(),
                last_activity_at=item['last_activity_at'].isoformat(),
                total_events=item['total_events'],
                page_views=item['page_views'],
                assistant_messages=item['assistant_messages'],
                contact_submissions=item['contact_submissions'],
                entry_page_path=item['entry_page_path'],
                last_page_path=item['last_page_path'],
                ip_address=item['ip_address'],
            )
            for item in sorted(visit_rollups.values(), key=lambda value: value['last_activity_at'], reverse=True)
        ]
        return visitors, visits

    def _build_conversation_activity_links(self, events: list[SiteEvent]) -> dict[str, dict[str, Any]]:
        links: dict[str, dict[str, Any]] = {}
        for event in events:
            if event.event_type != EventType.ASSISTANT_MESSAGE or not isinstance(event.metadata_json, dict):
                continue
            conversation_id = event.metadata_json.get('conversation_id')
            if not isinstance(conversation_id, str) or conversation_id in links:
                continue
            used_fallback = event.metadata_json.get('used_fallback')
            links[conversation_id] = {
                'visitor_id': event.visitor_id,
                'site_session_id': event.session_id,
                'page_path': event.page_path,
                'used_fallback': bool(used_fallback) if isinstance(used_fallback, bool) else None,
            }
        return links

    def _map_assistant_conversation(
        self, conversation: AssistantConversation, activity_link: dict[str, Any] | None = None
    ) -> AdminAssistantConversationSummaryOut:
        ordered_messages = sorted(conversation.messages, key=lambda item: item.created_at)
        user_messages = [item for item in ordered_messages if item.role == AssistantRole.USER]
        assistant_messages = [item for item in ordered_messages if item.role == AssistantRole.ASSISTANT]
        return AdminAssistantConversationSummaryOut(
            id=str(conversation.id),
            session_id=conversation.session_id,
            visitor_id=activity_link.get('visitor_id') if activity_link else None,
            site_session_id=activity_link.get('site_session_id') if activity_link else None,
            page_path=activity_link.get('page_path') if activity_link else None,
            started_at=conversation.started_at.isoformat(),
            last_message_at=conversation.last_message_at.isoformat(),
            total_messages=len(ordered_messages),
            user_message_count=len(user_messages),
            assistant_message_count=len(assistant_messages),
            used_fallback=activity_link.get('used_fallback') if activity_link else None,
            first_user_message=user_messages[0].message_text if user_messages else None,
            latest_assistant_message=assistant_messages[-1].message_text if assistant_messages else None,
        )

    def _map_media_file(self, media_file: MediaFile) -> AdminMediaFileOut:
        return AdminMediaFileOut(
            id=str(media_file.id),
            bucket_name=media_file.bucket_name,
            object_key=media_file.object_key,
            original_filename=media_file.original_filename,
            mime_type=media_file.mime_type,
            visibility=media_file.visibility.value,
            alt_text=media_file.alt_text,
            title=media_file.title,
            public_url=media_file.public_url,
            resolved_asset=self._map_media(media_file, alt=media_file.alt_text),
            created_at=media_file.created_at.isoformat(),
            updated_at=media_file.updated_at.isoformat(),
        )

    def _map_skill(self, skill: Skill) -> SkillSummaryOut:
        return SkillSummaryOut(
            id=str(skill.id),
            category_id=str(skill.category_id),
            name=skill.name,
            years_of_experience=skill.years_of_experience,
            icon_key=skill.icon_key,
            sort_order=skill.sort_order,
            is_highlighted=skill.is_highlighted,
        )

    def _map_media(self, media_file: MediaFile | None, alt: str | None = None) -> PublicMediaAssetOut | None:
        url = self.media_resolver.resolve(media_file)
        if media_file is None or url is None:
            return None
        return PublicMediaAssetOut(
            id=str(media_file.id),
            url=url,
            alt=media_file.alt_text or alt,
            file_name=media_file.original_filename,
            mime_type=media_file.mime_type,
            width=None,
            height=None,
        )

    def _slugify(self, value: str) -> str:
        cleaned = _slug_cleanup_pattern.sub('-', value.strip().lower()).strip('-')
        return cleaned or 'item'

    def _ensure_unique_slug(self, model, value: str, current_id: UUID | None = None) -> str:
        base_slug = self._slugify(value)
        slug = base_slug
        index = 2
        while True:
            query = select(model.id).where(model.slug == slug)
            if current_id is not None:
                query = query.where(model.id != current_id)
            exists = self.session.scalar(query.limit(1))
            if exists is None:
                return slug
            slug = f'{base_slug}-{index}'
            index += 1

    def _normalize_optional_text(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    def _parse_date(self, value: str | None) -> date | None:
        if value is None or not value.strip():
            return None
        return date.fromisoformat(value)

    def _parse_datetime(self, value: str | None) -> datetime | None:
        if value is None or not value.strip():
            return None
        raw = value.strip()
        if raw.endswith('Z'):
            raw = raw.replace('Z', '+00:00')
        parsed = datetime.fromisoformat(raw)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)

    def _optional_uuid(self, value: str | None) -> UUID | None:
        if value is None or not str(value).strip():
            return None
        return UUID(str(value).strip())

    def _required_uuid(self, value: str) -> UUID:
        return UUID(value.strip())
