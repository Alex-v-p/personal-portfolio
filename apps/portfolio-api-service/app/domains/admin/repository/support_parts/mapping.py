from __future__ import annotations

from app.db.models import AdminUser, BlogPost, ContactMessage, Experience, GithubSnapshot, MediaFile, NavigationItem, Profile, Project, SiteEvent, Skill, SkillCategory
from app.domains.admin.schema import (
    AdminBlogPostOut,
    AdminBlogTagOut,
    AdminContactMessageOut,
    AdminExperienceOut,
    AdminGithubContributionDayOut,
    AdminGithubSnapshotOut,
    AdminMediaFileOut,
    AdminMediaUsageSummaryOut,
    AdminNavigationItemOut,
    AdminProfileOut,
    AdminProjectOut,
    AdminSiteEventOut,
    AdminSocialLinkOut,
    AdminSkillCategoryOut,
    AdminSkillOut,
    AdminUserOut,
)
from app.domains.public_site.schema import PublicMediaAssetOut, SkillSummaryOut


class AdminRepositoryMappingMixin:
    def map_admin_user(self, admin_user: AdminUser) -> AdminUserOut:

        return AdminUserOut(
            id=str(admin_user.id),
            email=admin_user.email,
            display_name=admin_user.display_name,
            is_active=admin_user.is_active,
            created_at=admin_user.created_at.isoformat(),
        )

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

    def _map_media_file(self, media_file: MediaFile, usage_summary: AdminMediaUsageSummaryOut | None = None) -> AdminMediaFileOut:

        resolved_usage = usage_summary or AdminMediaUsageSummaryOut()
        return AdminMediaFileOut(
            id=str(media_file.id),
            bucket_name=media_file.bucket_name,
            object_key=media_file.object_key,
            original_filename=media_file.original_filename,
            stored_filename=media_file.stored_filename,
            mime_type=media_file.mime_type,
            file_size_bytes=media_file.file_size_bytes,
            checksum=media_file.checksum,
            description=media_file.description,
            visibility=media_file.visibility.value,
            alt_text=media_file.alt_text,
            title=media_file.title,
            public_url=media_file.public_url,
            folder=self._media_folder(media_file),
            resolved_asset=self._map_media(media_file, alt=media_file.alt_text),
            usage_summary=resolved_usage,
            can_delete=not resolved_usage.is_referenced,
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

    def _media_folder(self, media_file: MediaFile) -> str | None:
        object_key = (media_file.object_key or '').strip('/')
        if not object_key or '/' not in object_key:
            return None
        folder = object_key.rsplit('/', 1)[0].strip('/')
        return folder or None

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
