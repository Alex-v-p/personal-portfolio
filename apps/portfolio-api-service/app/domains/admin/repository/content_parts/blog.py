from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import BlogPost, BlogPostTag, BlogProtectedDocument, BlogProtectedDocumentGroup, MediaFile, PublicationStatus
from app.domains.admin.schema import AdminBlogPostOut, AdminBlogPostUpsertIn
from app.services.security import hash_password


class AdminBlogContentRepository:
    def list_blog_posts(self) -> list[AdminBlogPostOut]:
        posts = self.session.scalars(
            select(BlogPost)
            .options(
                selectinload(BlogPost.cover_image_file),
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
                selectinload(BlogPost.protected_document_groups)
                .selectinload(BlogProtectedDocumentGroup.documents)
                .selectinload(BlogProtectedDocument.media_file),
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
                selectinload(BlogPost.protected_document_groups)
                .selectinload(BlogProtectedDocumentGroup.documents)
                .selectinload(BlogProtectedDocument.media_file),
            )
            .where(BlogPost.id == post_id)
        )
        return self._map_blog_post(post) if post else None

    def create_blog_post(self, payload: AdminBlogPostUpsertIn) -> AdminBlogPostOut:
        slug_source = payload.slug or payload.title
        post = BlogPost(
            slug=self._ensure_unique_slug(BlogPost, slug_source),
            title=payload.title,
            title_nl=self._normalize_optional_text(payload.title_nl),
            excerpt=payload.excerpt,
            excerpt_nl=self._normalize_optional_text(payload.excerpt_nl),
            content_markdown=payload.content_markdown,
            content_markdown_nl=self._normalize_optional_text(payload.content_markdown_nl),
            cover_image_file_id=self._optional_uuid(payload.cover_image_file_id),
            cover_image_alt=self._normalize_optional_text(payload.cover_image_alt),
            cover_image_alt_nl=self._normalize_optional_text(payload.cover_image_alt_nl),
            reading_time_minutes=payload.reading_time_minutes,
            status=PublicationStatus(payload.status),
            is_featured=payload.is_featured,
            seo_title=self._normalize_optional_text(payload.seo_title),
            seo_title_nl=self._normalize_optional_text(payload.seo_title_nl),
            seo_description=self._normalize_optional_text(payload.seo_description),
            seo_description_nl=self._normalize_optional_text(payload.seo_description_nl),
            published_at=self._parse_datetime(payload.published_at),
        )
        self.session.add(post)
        self.session.flush()
        self._replace_blog_post_tags(post, payload.tag_ids)
        self._replace_blog_protected_document_groups(post, payload.protected_document_groups)
        self.session.commit()
        return self.get_blog_post(post.id)  # type: ignore[return-value]

    def update_blog_post(self, post_id: UUID, payload: AdminBlogPostUpsertIn) -> AdminBlogPostOut | None:
        post = self.session.scalar(
            select(BlogPost)
            .options(
                selectinload(BlogPost.protected_document_groups)
                .selectinload(BlogProtectedDocumentGroup.documents)
                .selectinload(BlogProtectedDocument.media_file),
            )
            .where(BlogPost.id == post_id)
        )
        if post is None:
            return None
        slug_source = payload.slug or payload.title
        post.slug = self._ensure_unique_slug(BlogPost, slug_source, current_id=post_id)
        post.title = payload.title
        post.title_nl = self._normalize_optional_text(payload.title_nl)
        post.excerpt = payload.excerpt
        post.excerpt_nl = self._normalize_optional_text(payload.excerpt_nl)
        post.content_markdown = payload.content_markdown
        post.content_markdown_nl = self._normalize_optional_text(payload.content_markdown_nl)
        post.cover_image_file_id = self._optional_uuid(payload.cover_image_file_id)
        post.cover_image_alt = self._normalize_optional_text(payload.cover_image_alt)
        post.cover_image_alt_nl = self._normalize_optional_text(payload.cover_image_alt_nl)
        post.reading_time_minutes = payload.reading_time_minutes
        post.status = PublicationStatus(payload.status)
        post.is_featured = payload.is_featured
        post.seo_title = self._normalize_optional_text(payload.seo_title)
        post.seo_title_nl = self._normalize_optional_text(payload.seo_title_nl)
        post.seo_description = self._normalize_optional_text(payload.seo_description)
        post.seo_description_nl = self._normalize_optional_text(payload.seo_description_nl)
        post.published_at = self._parse_datetime(payload.published_at)
        self._replace_blog_post_tags(post, payload.tag_ids)
        self._replace_blog_protected_document_groups(post, payload.protected_document_groups)
        self.session.commit()
        return self.get_blog_post(post_id)

    def delete_blog_post(self, post_id: UUID) -> bool:
        post = self.session.get(BlogPost, post_id)
        if post is None:
            return False
        self.session.delete(post)
        self.session.commit()
        return True

    def _replace_blog_protected_document_groups(self, post: BlogPost, groups_payload) -> None:
        existing_by_id = {str(group.id): group for group in post.protected_document_groups}
        existing_by_slug = {group.slug: group for group in post.protected_document_groups}
        used_group_ids: set[UUID] = set()
        used_slugs: set[str] = set()

        for index, group_payload in enumerate(groups_payload or []):
            documents_payload = [
                document
                for document in (self._payload_value(group_payload, 'documents', []) or [])
                if self._payload_value(document, 'media_file_id')
            ]

            raw_id = self._payload_value(group_payload, 'id')
            raw_slug = self._normalize_optional_text(self._payload_value(group_payload, 'slug'))
            raw_title = self._normalize_optional_text(self._payload_value(group_payload, 'title'))
            if raw_title is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Protected document cards need a title before saving.')

            group = existing_by_id.get(str(raw_id or '')) or (existing_by_slug.get(raw_slug) if raw_slug else None)
            is_new_group = group is None
            if is_new_group:
                group = BlogProtectedDocumentGroup(blog_post_id=post.id)

            slug_source = raw_slug or raw_title or f'{post.slug}-documents'
            group.slug = self._ensure_unique_protected_document_group_slug(slug_source, current_id=group.id, used_slugs=used_slugs)
            used_slugs.add(group.slug)
            group.title = raw_title
            group.title_nl = self._normalize_optional_text(self._payload_value(group_payload, 'title_nl'))
            group.description = self._normalize_optional_text(self._payload_value(group_payload, 'description'))
            group.description_nl = self._normalize_optional_text(self._payload_value(group_payload, 'description_nl'))
            group.is_enabled = bool(self._payload_value(group_payload, 'is_enabled', True))
            raw_sort_order = self._payload_value(group_payload, 'sort_order')
            group.sort_order = raw_sort_order if raw_sort_order is not None else index

            new_password = self._normalize_optional_text(self._payload_value(group_payload, 'new_password'))
            if new_password and len(new_password) < 8:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Protected document card "{group.title}" needs a password of at least 8 characters.',
                )
            if new_password:
                group.password_hash = hash_password(new_password)
            elif group.password_hash is None and group.is_enabled:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Protected document card "{group.title}" needs an access password before it can be enabled.',
                )

            if group.is_enabled and not documents_payload:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Protected document card "{group.title}" needs at least one selected document before it can be enabled.',
                )

            if is_new_group:
                post.protected_document_groups.append(group)

            self._replace_blog_protected_documents(group, documents_payload)
            self.session.flush()
            used_group_ids.add(group.id)

        for group in list(post.protected_document_groups):
            if group.id not in used_group_ids:
                self.session.delete(group)
        self.session.flush()

    def _replace_blog_protected_documents(self, group: BlogProtectedDocumentGroup, documents_payload) -> None:
        group.documents.clear()
        seen_media_file_ids: set[UUID] = set()

        for index, document_payload in enumerate(sorted(documents_payload, key=lambda item: self._payload_value(item, 'sort_order', 0) or 0)):
            raw_media_file_id = self._payload_value(document_payload, 'media_file_id')
            media_file_id = self._required_uuid(raw_media_file_id)  # type: ignore[arg-type]
            if media_file_id in seen_media_file_ids:
                continue
            seen_media_file_ids.add(media_file_id)
            if self.session.get(MediaFile, media_file_id) is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Selected protected document media file does not exist.')
            raw_sort_order = self._payload_value(document_payload, 'sort_order')
            group.documents.append(
                BlogProtectedDocument(
                    media_file_id=media_file_id,
                    title=self._normalize_optional_text(self._payload_value(document_payload, 'title')),
                    title_nl=self._normalize_optional_text(self._payload_value(document_payload, 'title_nl')),
                    sort_order=raw_sort_order if raw_sort_order is not None else index,
                )
            )

    def _ensure_unique_protected_document_group_slug(self, value: str, *, current_id: UUID | None, used_slugs: set[str]) -> str:
        base_slug = self._slugify(value)
        slug = base_slug
        index = 2
        while True:
            candidate = self._ensure_unique_slug(BlogProtectedDocumentGroup, slug, current_id=current_id)
            if candidate not in used_slugs:
                return candidate
            slug = f'{base_slug}-{index}'
            index += 1

    @staticmethod
    def _payload_value(payload, snake_name: str, default=None):
        if isinstance(payload, dict):
            camel_name = snake_name.split('_')[0] + ''.join(part.capitalize() for part in snake_name.split('_')[1:])
            return payload.get(snake_name, payload.get(camel_name, default))
        return getattr(payload, snake_name, default)
