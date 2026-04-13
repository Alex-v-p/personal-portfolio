from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import BlogPost, BlogPostTag, PublicationStatus
from app.schemas.admin import AdminBlogPostOut, AdminBlogPostUpsertIn


class AdminBlogContentRepository:
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
            title=payload.title,
            excerpt=payload.excerpt,
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
        post.title = payload.title
        post.excerpt = payload.excerpt
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
