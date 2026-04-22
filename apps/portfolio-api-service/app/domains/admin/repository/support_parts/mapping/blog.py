from __future__ import annotations

from app.db.models import BlogPost
from app.domains.admin.schema import AdminBlogPostOut, AdminBlogTagOut


class AdminRepositoryBlogMappingMixin:
    def _map_blog_post(self, post: BlogPost) -> AdminBlogPostOut:
        ordered_tags = sorted((link.tag for link in post.tag_links), key=lambda tag: tag.name.lower())

        return AdminBlogPostOut(
            id=str(post.id),
            slug=post.slug,
            title=post.title,
            title_nl=post.title_nl,
            excerpt=post.excerpt,
            excerpt_nl=post.excerpt_nl,
            content_markdown=post.content_markdown,
            content_markdown_nl=post.content_markdown_nl,
            cover_image_file_id=str(post.cover_image_file_id) if post.cover_image_file_id else None,
            cover_image_alt=post.cover_image_alt,
            cover_image_alt_nl=post.cover_image_alt_nl,
            cover_image=self._map_media(post.cover_image_file, alt=post.cover_image_alt or f'{post.title} cover image'),
            reading_time_minutes=post.reading_time_minutes,
            status=post.status.value,
            is_featured=post.is_featured,
            published_at=post.published_at.isoformat() if post.published_at else None,
            seo_title=post.seo_title,
            seo_title_nl=post.seo_title_nl,
            seo_description=post.seo_description,
            seo_description_nl=post.seo_description_nl,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            tag_ids=[str(tag.id) for tag in ordered_tags],
            tag_names=[tag.name for tag in ordered_tags],
            tags=[AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug) for tag in ordered_tags],
        )
