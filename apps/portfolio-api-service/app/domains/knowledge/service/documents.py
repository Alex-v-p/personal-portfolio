from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import (
    BlogPost,
    BlogPostTag,
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
            documents.append(self._build_profile_document(profile))

        projects = self.session.scalars(
            select(Project)
            .options(selectinload(Project.skill_links).selectinload(ProjectSkill.skill))
            .where(Project.state != ProjectState.ARCHIVED, Project.published_at <= publication_cutoff)
            .order_by(Project.sort_order.asc(), Project.published_at.desc())
        ).all()
        documents.extend(self._build_project_document(project) for project in projects)

        experiences = self.session.scalars(
            select(Experience)
            .options(selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill))
            .order_by(Experience.sort_order.asc(), Experience.start_date.desc())
        ).all()
        documents.extend(self._build_experience_document(item) for item in experiences)

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
        documents.extend(self._build_blog_post_document(post) for post in blog_posts)
        return documents

    def _build_profile_document(self, profile: Profile) -> KnowledgeDocument:
        full_name = f'{profile.first_name} {profile.last_name}'.strip()
        social_links = [f'- {link.label}: {link.url}' for link in sorted(profile.social_links, key=lambda item: item.sort_order)]
        content = '\n\n'.join(
            part
            for part in [
                f'# {full_name}',
                profile.headline,
                profile.short_intro,
                profile.long_bio or '',
                f'Location: {profile.location}' if profile.location else '',
                f'Email: {profile.email}' if profile.email else '',
                f'Primary CTA: {profile.cta_primary_label} — {profile.cta_primary_url}' if profile.cta_primary_label and profile.cta_primary_url else '',
                '## Social links\n' + '\n'.join(social_links) if social_links else '',
            ]
            if part
        )
        return KnowledgeDocument(
            id=uuid4(),
            source_type=KnowledgeSourceType.PROFILE,
            source_id=profile.id,
            title=full_name,
            canonical_url='/',
            content_markdown=content,
            content_platform='portfolio',
            metadata_json={
                'headline': profile.headline,
                'location': profile.location,
                'social_platforms': [link.platform for link in profile.social_links],
            },
        )

    def _build_project_document(self, project: Project) -> KnowledgeDocument:
        skills = [link.skill.name for link in sorted(project.skill_links, key=lambda item: item.skill.sort_order) if link.skill is not None]
        content = '\n\n'.join(
            part
            for part in [
                f'# {project.title}',
                project.teaser,
                project.summary or '',
                project.description_markdown or '',
                f'Status: {project.status}',
                f'State: {project.state.value}',
                f'Duration: {project.duration_label}',
                f'Company: {project.company_name}' if project.company_name else '',
                f'GitHub: {project.github_url}' if project.github_url else '',
                f'Demo: {project.demo_url}' if project.demo_url else '',
                '## Skills\n' + ', '.join(skills) if skills else '',
            ]
            if part
        )
        return KnowledgeDocument(
            id=uuid4(),
            source_type=KnowledgeSourceType.PROJECT,
            source_id=project.id,
            title=project.title,
            canonical_url='/projects',
            content_markdown=content,
            content_platform='portfolio',
            metadata_json={
                'slug': project.slug,
                'skills': skills,
                'status': project.status,
                'state': project.state.value,
                'company_name': project.company_name,
            },
        )

    def _build_experience_document(self, experience: Experience) -> KnowledgeDocument:
        skills = [link.skill.name for link in sorted(experience.skill_links, key=lambda item: item.skill.sort_order) if link.skill is not None]
        title = f'{experience.role_title} at {experience.organization_name}'
        content = '\n\n'.join(
            part
            for part in [
                f'# {title}',
                experience.summary,
                experience.description_markdown or '',
                f'Type: {experience.experience_type}',
                f'Location: {experience.location}' if experience.location else '',
                f'Start date: {experience.start_date.isoformat()}',
                f'End date: {experience.end_date.isoformat()}' if experience.end_date else ('Current role' if experience.is_current else ''),
                '## Skills\n' + ', '.join(skills) if skills else '',
            ]
            if part
        )
        return KnowledgeDocument(
            id=uuid4(),
            source_type=KnowledgeSourceType.EXPERIENCE,
            source_id=experience.id,
            title=title,
            canonical_url='/experience',
            content_markdown=content,
            content_platform='portfolio',
            metadata_json={
                'organization_name': experience.organization_name,
                'role_title': experience.role_title,
                'skills': skills,
                'experience_type': experience.experience_type,
            },
        )

    def _build_blog_post_document(self, post: BlogPost) -> KnowledgeDocument:
        tags = [link.tag.name for link in sorted(post.tag_links, key=lambda item: item.tag.name) if link.tag is not None]
        content = '\n\n'.join(
            part
            for part in [
                f'# {post.title}',
                post.excerpt,
                post.content_markdown,
                f'Reading time: {post.reading_time_minutes} minutes' if post.reading_time_minutes else '',
                f'Status: {post.status.value}',
                '## Tags\n' + ', '.join(tags) if tags else '',
                post.seo_description or '',
            ]
            if part
        )
        return KnowledgeDocument(
            id=uuid4(),
            source_type=KnowledgeSourceType.BLOG_POST,
            source_id=post.id,
            title=post.title,
            canonical_url=f'/blog/{post.slug}',
            content_markdown=content,
            content_platform='portfolio',
            metadata_json={
                'slug': post.slug,
                'tags': tags,
                'status': post.status.value,
                'seo_title': post.seo_title,
            },
        )
