from __future__ import annotations

from datetime import UTC, date, datetime
import re
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.db.models import (
    AdminUser,
    BlogPost,
    BlogPostTag,
    BlogTag,
    ContactMessage,
    MediaFile,
    Profile,
    Project,
    ProjectImage,
    ProjectSkill,
    ProjectState,
    PublicationStatus,
    Skill,
    SocialLink,
)
from app.schemas.admin import (
    AdminBlogPostOut,
    AdminBlogPostUpsertIn,
    AdminBlogTagOut,
    AdminContactMessageOut,
    AdminDashboardSummaryOut,
    AdminMediaFileOut,
    AdminProfileOut,
    AdminProfileUpdateIn,
    AdminProjectOut,
    AdminProjectUpsertIn,
    AdminReferenceDataOut,
    AdminSocialLinkOut,
    AdminUserOut,
)
from app.schemas.public import PublicMediaAssetOut, SkillSummaryOut
from app.services.media_resolver import PublicMediaUrlResolver

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

    def get_dashboard_summary(self) -> AdminDashboardSummaryOut:
        return AdminDashboardSummaryOut(
            projects=self.session.scalar(select(func.count(Project.id))) or 0,
            blog_posts=self.session.scalar(select(func.count(BlogPost.id))) or 0,
            unread_messages=self.session.scalar(select(func.count(ContactMessage.id)).where(ContactMessage.is_read.is_(False))) or 0,
            skills=self.session.scalar(select(func.count(Skill.id))) or 0,
            media_files=self.session.scalar(select(func.count(MediaFile.id))) or 0,
        )

    def get_reference_data(self) -> AdminReferenceDataOut:
        skills = self.session.scalars(select(Skill).order_by(Skill.sort_order.asc(), Skill.name.asc())).all()
        media_files = self.session.scalars(select(MediaFile).order_by(MediaFile.created_at.desc())).all()
        blog_tags = self.session.scalars(select(BlogTag).order_by(BlogTag.name.asc())).all()
        return AdminReferenceDataOut(
            skills=[self._map_skill(skill) for skill in skills],
            media_files=[self._map_media_file(media_file) for media_file in media_files],
            blog_tags=[AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug) for tag in blog_tags],
            project_states=['published', 'archived', 'completed', 'paused'],
            publication_statuses=['draft', 'published', 'archived'],
        )

    def list_projects(self) -> list[AdminProjectOut]:
        projects = self.session.scalars(
            select(Project)
            .options(
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
                selectinload(Project.cover_image_file),
            )
            .order_by(Project.sort_order.asc(), Project.created_at.desc())
        ).all()
        return [self._map_project(project) for project in projects]

    def get_project(self, project_id: UUID) -> AdminProjectOut | None:
        project = self.session.scalar(
            select(Project)
            .options(
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
                selectinload(Project.images).selectinload(ProjectImage.image_file),
                selectinload(Project.cover_image_file),
            )
            .where(Project.id == project_id)
        )
        return self._map_project(project) if project else None

    def create_project(self, payload: AdminProjectUpsertIn) -> AdminProjectOut:
        project = Project(
            slug=self._ensure_unique_slug(Project, payload.slug or payload.title),
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
        self.session.refresh(project)
        return self.get_project(project.id)  # type: ignore[return-value]

    def update_project(self, project_id: UUID, payload: AdminProjectUpsertIn) -> AdminProjectOut | None:
        project = self.session.get(Project, project_id)
        if project is None:
            return None

        proposed_slug = payload.slug or payload.title
        project.slug = self._ensure_unique_slug(Project, proposed_slug, current_id=project.id)
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
        return self.get_project(project.id)

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
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
                selectinload(BlogPost.cover_image_file),
            )
            .order_by(BlogPost.created_at.desc())
        ).all()
        return [self._map_blog_post(post) for post in posts]

    def get_blog_post(self, post_id: UUID) -> AdminBlogPostOut | None:
        post = self.session.scalar(
            select(BlogPost)
            .options(
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
                selectinload(BlogPost.cover_image_file),
            )
            .where(BlogPost.id == post_id)
        )
        return self._map_blog_post(post) if post else None

    def create_blog_post(self, payload: AdminBlogPostUpsertIn) -> AdminBlogPostOut:
        now = datetime.now(UTC)
        status = PublicationStatus(payload.status)
        published_at = self._parse_datetime(payload.published_at)
        if status == PublicationStatus.PUBLISHED and published_at is None:
            published_at = now
        post = BlogPost(
            slug=self._ensure_unique_slug(BlogPost, payload.slug or payload.title),
            title=payload.title.strip(),
            excerpt=payload.excerpt.strip(),
            content_markdown=payload.content_markdown.strip(),
            cover_image_file_id=self._optional_uuid(payload.cover_image_file_id),
            cover_image_alt=self._normalize_optional_text(payload.cover_image_alt),
            reading_time_minutes=payload.reading_time_minutes,
            status=status,
            is_featured=payload.is_featured,
            published_at=published_at,
            seo_title=self._normalize_optional_text(payload.seo_title),
            seo_description=self._normalize_optional_text(payload.seo_description),
        )
        self.session.add(post)
        self.session.flush()
        self._replace_blog_post_tags(post, payload.tag_names)
        self.session.commit()
        return self.get_blog_post(post.id)  # type: ignore[return-value]

    def update_blog_post(self, post_id: UUID, payload: AdminBlogPostUpsertIn) -> AdminBlogPostOut | None:
        post = self.session.get(BlogPost, post_id)
        if post is None:
            return None
        status = PublicationStatus(payload.status)
        post.slug = self._ensure_unique_slug(BlogPost, payload.slug or payload.title, current_id=post.id)
        post.title = payload.title.strip()
        post.excerpt = payload.excerpt.strip()
        post.content_markdown = payload.content_markdown.strip()
        post.cover_image_file_id = self._optional_uuid(payload.cover_image_file_id)
        post.cover_image_alt = self._normalize_optional_text(payload.cover_image_alt)
        post.reading_time_minutes = payload.reading_time_minutes
        post.status = status
        post.is_featured = payload.is_featured
        parsed_published_at = self._parse_datetime(payload.published_at)
        if parsed_published_at is not None:
            post.published_at = parsed_published_at
        elif status == PublicationStatus.PUBLISHED and post.published_at is None:
            post.published_at = datetime.now(UTC)
        elif status == PublicationStatus.DRAFT:
            post.published_at = None
        post.seo_title = self._normalize_optional_text(payload.seo_title)
        post.seo_description = self._normalize_optional_text(payload.seo_description)
        self._replace_blog_post_tags(post, payload.tag_names)
        self.session.commit()
        return self.get_blog_post(post.id)

    def delete_blog_post(self, post_id: UUID) -> bool:
        post = self.session.get(BlogPost, post_id)
        if post is None:
            return False
        self.session.delete(post)
        self.session.commit()
        return True

    def get_profile(self) -> AdminProfileOut | None:
        profile = self.session.scalar(
            select(Profile)
            .options(
                selectinload(Profile.social_links),
                selectinload(Profile.avatar_file),
                selectinload(Profile.hero_image_file),
                selectinload(Profile.resume_file),
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

    def _replace_blog_post_tags(self, post: BlogPost, tag_names: list[str]) -> None:
        normalized_names = []
        seen = set()
        for raw_name in tag_names:
            name = raw_name.strip()
            if not name:
                continue
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)
            normalized_names.append(name)

        post.tag_links.clear()
        self.session.flush()
        for name in normalized_names:
            slug = self._slugify(name)
            tag = self.session.scalar(select(BlogTag).where(BlogTag.slug == slug))
            if tag is None:
                tag = BlogTag(name=name, slug=slug)
                self.session.add(tag)
                self.session.flush()
            post.tag_links.append(BlogPostTag(tag_id=tag.id))

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
            tag_names=[tag.name for tag in ordered_tags],
            tags=[AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug) for tag in ordered_tags],
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
