from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import (
    BlogPost,
    BlogPostTag,
    AssistantContextNote,
    Experience,
    ExperienceSkill,
    KnowledgeDocument,
    KnowledgeSourceType,
    Profile,
    Project,
    ProjectSkill,
    ProjectState,
    PublicationStatus,
)

SUPPORTED_KNOWLEDGE_LOCALES: tuple[str, ...] = ('en', 'nl')
DEFAULT_KNOWLEDGE_LOCALE = 'en'


class KnowledgeDocumentBuilder:
    def __init__(self, session: Session) -> None:
        self.session = session

    def build_documents(self) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        publication_cutoff = datetime.now(UTC)
        profile = self.session.scalar(
            select(Profile).options(selectinload(Profile.social_links)).where(Profile.is_public.is_(True)).order_by(Profile.created_at.desc())
        )
        if profile is not None:
            documents.extend(self._build_profile_documents(profile))

        projects = self.session.scalars(
            select(Project)
            .options(selectinload(Project.skill_links).selectinload(ProjectSkill.skill))
            .where(Project.state != ProjectState.ARCHIVED, Project.published_at <= publication_cutoff)
            .order_by(Project.sort_order.asc(), Project.published_at.desc())
        ).all()
        for project in projects:
            documents.extend(self._build_project_documents(project))

        experiences = self.session.scalars(
            select(Experience)
            .options(selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill))
            .order_by(Experience.sort_order.asc(), Experience.start_date.desc())
        ).all()
        for item in experiences:
            documents.extend(self._build_experience_documents(item))

        blog_posts = self.session.scalars(
            select(BlogPost)
            .options(selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag))
            .where(
                BlogPost.status == PublicationStatus.PUBLISHED,
                BlogPost.published_at.is_not(None),
                BlogPost.published_at <= publication_cutoff,
            )
            .order_by(BlogPost.published_at.desc().nullslast(), BlogPost.created_at.desc())
        ).all()
        for post in blog_posts:
            documents.extend(self._build_blog_post_documents(post))

        context_notes = self.session.scalars(
            select(AssistantContextNote)
            .where(AssistantContextNote.is_active.is_(True))
            .order_by(AssistantContextNote.sort_order.asc(), AssistantContextNote.title.asc())
        ).all()
        for note in context_notes:
            documents.extend(self._build_assistant_note_documents(note))
        return documents

    def _build_profile_documents(self, profile: Profile) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        full_name = f'{profile.first_name} {profile.last_name}'.strip()
        social_links = [f'- {link.label}: {link.url}' for link in sorted(profile.social_links, key=lambda item: item.sort_order)]

        for locale in SUPPORTED_KNOWLEDGE_LOCALES:
            headline = self._localized(profile, 'headline', locale)
            short_intro = self._localized(profile, 'short_intro', locale)
            long_bio = self._localized(profile, 'long_bio', locale)
            primary_cta_label = self._localized(profile, 'cta_primary_label', locale)
            content = '\n\n'.join(
                part
                for part in [
                    f'# {full_name}',
                    headline,
                    short_intro,
                    long_bio,
                    f'Location: {profile.location}' if profile.location else '',
                    f'Email: {profile.email}' if profile.email else '',
                    f'Primary CTA: {primary_cta_label} — {profile.cta_primary_url}' if primary_cta_label and profile.cta_primary_url else '',
                    '## Social links\n' + '\n'.join(social_links) if social_links else '',
                ]
                if part
            )
            documents.append(
                KnowledgeDocument(
                    id=uuid4(),
                    source_type=KnowledgeSourceType.PROFILE,
                    source_id=profile.id,
                    title=full_name,
                    canonical_url='/',
                    content_markdown=content,
                    content_platform='portfolio',
                    metadata_json={
                        'locale': locale,
                        'headline': headline,
                        'location': profile.location,
                        'social_platforms': [link.platform for link in profile.social_links],
                    },
                )
            )
        return documents

    def _build_project_documents(self, project: Project) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        skills = [link.skill.name for link in sorted(project.skill_links, key=lambda item: item.skill.sort_order) if link.skill is not None]

        for locale in SUPPORTED_KNOWLEDGE_LOCALES:
            title = self._localized(project, 'title', locale)
            teaser = self._localized(project, 'teaser', locale)
            summary = self._localized(project, 'summary', locale)
            description_markdown = self._localized(project, 'description_markdown', locale)
            status = self._localized(project, 'status', locale)
            duration_label = self._localized(project, 'duration_label', locale)
            content = '\n\n'.join(
                part
                for part in [
                    f'# {title}',
                    teaser,
                    summary,
                    description_markdown,
                    f'Status: {status}' if status else '',
                    f'State: {project.state.value}',
                    f'Duration: {duration_label}' if duration_label else '',
                    f'Company: {project.company_name}' if project.company_name else '',
                    f'GitHub: {project.github_url}' if project.github_url else '',
                    f'Demo: {project.demo_url}' if project.demo_url else '',
                    '## Skills\n' + ', '.join(skills) if skills else '',
                ]
                if part
            )
            documents.append(
                KnowledgeDocument(
                    id=uuid4(),
                    source_type=KnowledgeSourceType.PROJECT,
                    source_id=project.id,
                    title=title,
                    canonical_url=project.github_url or '/projects',
                    content_markdown=content,
                    content_platform='portfolio',
                    metadata_json={
                        'locale': locale,
                        'slug': project.slug,
                        'skills': skills,
                        'status': status,
                        'state': project.state.value,
                        'company_name': project.company_name,
                    },
                )
            )
        return documents

    def _build_experience_documents(self, experience: Experience) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        skills = [link.skill.name for link in sorted(experience.skill_links, key=lambda item: item.skill.sort_order) if link.skill is not None]

        for locale in SUPPORTED_KNOWLEDGE_LOCALES:
            role_title = self._localized(experience, 'role_title', locale)
            summary = self._localized(experience, 'summary', locale)
            description_markdown = self._localized(experience, 'description_markdown', locale)
            title = f'{role_title} at {experience.organization_name}'
            content = '\n\n'.join(
                part
                for part in [
                    f'# {title}',
                    summary,
                    description_markdown,
                    f'Type: {experience.experience_type}',
                    f'Location: {experience.location}' if experience.location else '',
                    f'Start date: {experience.start_date.isoformat()}',
                    f'End date: {experience.end_date.isoformat()}' if experience.end_date else ('Current role' if experience.is_current else ''),
                    '## Skills\n' + ', '.join(skills) if skills else '',
                ]
                if part
            )
            documents.append(
                KnowledgeDocument(
                    id=uuid4(),
                    source_type=KnowledgeSourceType.EXPERIENCE,
                    source_id=experience.id,
                    title=title,
                    canonical_url='/experience',
                    content_markdown=content,
                    content_platform='portfolio',
                    metadata_json={
                        'locale': locale,
                        'organization_name': experience.organization_name,
                        'role_title': role_title,
                        'skills': skills,
                        'experience_type': experience.experience_type,
                    },
                )
            )
        return documents

    def _build_blog_post_documents(self, post: BlogPost) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        tags = [link.tag.name for link in sorted(post.tag_links, key=lambda item: item.tag.name) if link.tag is not None]

        for locale in SUPPORTED_KNOWLEDGE_LOCALES:
            title = self._localized(post, 'title', locale)
            excerpt = self._localized(post, 'excerpt', locale)
            content_markdown = self._localized(post, 'content_markdown', locale)
            seo_description = self._localized(post, 'seo_description', locale)
            seo_title = self._localized(post, 'seo_title', locale)
            content = '\n\n'.join(
                part
                for part in [
                    f'# {title}',
                    excerpt,
                    content_markdown,
                    f'Reading time: {post.reading_time_minutes} minutes' if post.reading_time_minutes else '',
                    f'Status: {post.status.value}',
                    '## Tags\n' + ', '.join(tags) if tags else '',
                    seo_description,
                ]
                if part
            )
            documents.append(
                KnowledgeDocument(
                    id=uuid4(),
                    source_type=KnowledgeSourceType.BLOG_POST,
                    source_id=post.id,
                    title=title,
                    canonical_url=f'/blog/{post.slug}',
                    content_markdown=content,
                    content_platform='portfolio',
                    metadata_json={
                        'locale': locale,
                        'slug': post.slug,
                        'tags': tags,
                        'status': post.status.value,
                        'seo_title': seo_title,
                    },
                )
            )
        return documents

    def _build_assistant_note_documents(self, note: AssistantContextNote) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        for locale in SUPPORTED_KNOWLEDGE_LOCALES:
            title = self._localized(note, 'title', locale)
            content_markdown = self._localized(note, 'content_markdown', locale)
            if not title or not content_markdown:
                continue
            content = '\n\n'.join(
                part
                for part in [
                    f'# {title}',
                    f'Category: {note.category}',
                    content_markdown,
                ]
                if part
            )
            documents.append(
                KnowledgeDocument(
                    id=uuid4(),
                    source_type=KnowledgeSourceType.ASSISTANT_NOTE,
                    source_id=note.id,
                    title=title,
                    canonical_url=None,
                    content_markdown=content,
                    content_platform='assistant_context',
                    metadata_json={
                        'locale': locale,
                        'category': note.category,
                        'visibility': 'assistant_only',
                    },
                )
            )
        return documents

    def _localized(self, record: object, field_name: str, locale: str) -> str:
        if locale != DEFAULT_KNOWLEDGE_LOCALE:
            localized_value = getattr(record, f'{field_name}_{locale}', None)
            if isinstance(localized_value, str):
                localized_value = localized_value.strip()
            if localized_value:
                return localized_value
        value = getattr(record, field_name, '')
        return value.strip() if isinstance(value, str) else ''
