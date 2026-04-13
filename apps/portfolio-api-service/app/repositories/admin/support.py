from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
import re
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

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
    NavigationItem,
    Profile,
    Project,
    ProjectImage,
    ProjectSkill,
    SiteEvent,
    Skill,
    SkillCategory,
)
from app.schemas.admin import (
    AdminAssistantConversationSummaryOut,
    AdminBlogPostOut,
    AdminBlogTagOut,
    AdminContactMessageOut,
    AdminExperienceOut,
    AdminGithubContributionDayOut,
    AdminGithubSnapshotOut,
    AdminGithubSnapshotUpsertIn,
    AdminMediaFileOut,
    AdminNavigationItemOut,
    AdminProfileOut,
    AdminProjectOut,
    AdminSiteEventOut,
    AdminSocialLinkOut,
    AdminSkillCategoryOut,
    AdminSkillOut,
    AdminUserOut,
    AdminVisitSessionSummaryOut,
    AdminVisitorActivitySummaryOut,
)
from app.schemas.public import PublicMediaAssetOut, SkillSummaryOut
from app.services.media_resolver import PublicMediaUrlResolver

_slug_cleanup_pattern = re.compile(r'[^a-z0-9]+')


class AdminRepositorySupport:
    def __init__(self, session: Session) -> None:

        self.session = session

        self.media_resolver = PublicMediaUrlResolver(allow_non_public=True)



    def map_admin_user(self, admin_user: AdminUser) -> AdminUserOut:

        return AdminUserOut(

            id=str(admin_user.id),

            email=admin_user.email,

            display_name=admin_user.display_name,

            is_active=admin_user.is_active,

            created_at=admin_user.created_at.isoformat(),

        )



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
