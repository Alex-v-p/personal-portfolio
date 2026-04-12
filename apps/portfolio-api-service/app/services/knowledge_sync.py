from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from uuid import uuid4

import httpx
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.db.models import (
    BlogPost,
    BlogPostTag,
    Experience,
    ExperienceSkill,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeSourceType,
    Profile,
    Project,
    ProjectSkill,
)


@dataclass(slots=True)
class KnowledgeSyncReport:
    total_documents: int
    total_chunks: int
    documents_by_source_type: dict[str, int]
    latest_updated_at: str | None


class KnowledgeEmbeddingClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._disabled_reason: str | None = None

    @property
    def is_enabled(self) -> bool:
        return self.settings.knowledge_embedding_backend.strip().lower() not in {'', 'none', 'disabled'} and self._disabled_reason is None

    def embed(self, text: str) -> str | None:
        if not text.strip() or not self.is_enabled:
            return None

        backend = self.settings.knowledge_embedding_backend.strip().lower()
        try:
            if backend == 'ollama':
                vector = self._embed_with_ollama(text)
            elif backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
                vector = self._embed_with_openai_compatible(text)
            else:
                self._disabled_reason = f'Unsupported embedding backend: {backend}'
                return None
        except Exception as exc:  # pragma: no cover - graceful degradation for missing model/provider
            self._disabled_reason = str(exc)
            return None

        return self._format_vector(vector) if vector else None

    def _embed_with_ollama(self, text: str) -> list[float]:
        with httpx.Client(timeout=self.settings.knowledge_embedding_timeout_seconds) as client:
            response = client.post(
                f"{self.settings.knowledge_embedding_base_url.rstrip('/')}/api/embed",
                json={
                    'model': self.settings.knowledge_embedding_model,
                    'input': text,
                },
            )
            response.raise_for_status()
            payload = response.json()
        embeddings = payload.get('embeddings') or []
        if embeddings and isinstance(embeddings[0], list):
            return [float(value) for value in embeddings[0]]
        embedding = payload.get('embedding') or []
        return [float(value) for value in embedding]

    def _embed_with_openai_compatible(self, text: str) -> list[float]:
        headers = {'Content-Type': 'application/json'}
        if self.settings.knowledge_embedding_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.knowledge_embedding_api_key.strip()}"
        with httpx.Client(timeout=self.settings.knowledge_embedding_timeout_seconds) as client:
            response = client.post(
                f"{self.settings.knowledge_embedding_base_url.rstrip('/')}/v1/embeddings",
                headers=headers,
                json={
                    'model': self.settings.knowledge_embedding_model,
                    'input': text,
                },
            )
            response.raise_for_status()
            payload = response.json()
        data = payload.get('data') or []
        if not data:
            return []
        embedding = data[0].get('embedding') or []
        return [float(value) for value in embedding]

    def _format_vector(self, vector: list[float]) -> str:
        if not vector:
            return '[]'
        norm = math.sqrt(sum(value * value for value in vector))
        normalized = vector if norm == 0 else [value / norm for value in vector]
        return '[' + ','.join(f'{value:.8f}' for value in normalized) + ']'


class KnowledgeSyncService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.embedding_client = KnowledgeEmbeddingClient()

    def rebuild(self) -> KnowledgeSyncReport:
        self.session.execute(delete(KnowledgeChunk))
        self.session.execute(delete(KnowledgeDocument))
        self.session.flush()

        documents = self._build_documents()
        chunk_count = 0
        for document in documents:
            self.session.add(document)
            self.session.flush()
            chunks = self._chunk_markdown(document.content_markdown)
            for index, chunk_text in enumerate(chunks):
                self.session.add(
                    KnowledgeChunk(
                        id=uuid4(),
                        document_id=document.id,
                        chunk_index=index,
                        chunk_text=chunk_text,
                        embedding_vector=self.embedding_client.embed(chunk_text),
                        metadata_json={'source_type': document.source_type.value, **(document.metadata_json or {})},
                    )
                )
                chunk_count += 1

        self.session.commit()
        return self.get_status()

    def get_status(self) -> KnowledgeSyncReport:
        documents = self.session.scalars(select(KnowledgeDocument).order_by(KnowledgeDocument.updated_at.desc())).all()
        chunks = self.session.scalars(select(KnowledgeChunk)).all()
        by_source = Counter(
            document.source_type.value if hasattr(document.source_type, 'value') else str(document.source_type)
            for document in documents
        )
        latest_updated_at = documents[0].updated_at.isoformat() if documents else None
        return KnowledgeSyncReport(
            total_documents=len(documents),
            total_chunks=len(chunks),
            documents_by_source_type=dict(sorted(by_source.items())),
            latest_updated_at=latest_updated_at,
        )

    def _build_documents(self) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        profile = self.session.scalar(
            select(Profile).options(selectinload(Profile.social_links)).order_by(Profile.created_at.desc())
        )
        if profile is not None:
            documents.append(self._build_profile_document(profile))

        projects = self.session.scalars(
            select(Project)
            .options(selectinload(Project.skill_links).selectinload(ProjectSkill.skill))
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

    def _chunk_markdown(self, markdown: str, chunk_target_chars: int = 550) -> list[str]:
        normalized = re.sub(r'\n{3,}', '\n\n', markdown or '').strip()
        if not normalized:
            return []
        blocks = [block.strip() for block in normalized.split('\n\n') if block.strip()]
        chunks: list[str] = []
        current = ''
        for block in blocks:
            candidate = f'{current}\n\n{block}'.strip() if current else block
            if len(candidate) <= chunk_target_chars:
                current = candidate
                continue
            if current:
                chunks.append(current)
                current = ''
            if len(block) <= chunk_target_chars:
                current = block
                continue
            sentences = re.split(r'(?<=[.!?])\s+', block)
            segment = ''
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                candidate_sentence = f'{segment} {sentence}'.strip() if segment else sentence
                if len(candidate_sentence) <= chunk_target_chars:
                    segment = candidate_sentence
                    continue
                if segment:
                    chunks.append(segment)
                segment = sentence
            if segment:
                current = segment
        if current:
            chunks.append(current)
        return chunks
