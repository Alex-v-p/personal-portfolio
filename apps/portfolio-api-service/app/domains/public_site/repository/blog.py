from __future__ import annotations

from sqlalchemy.orm import selectinload

from app.db.models import BlogPost, BlogPostTag
from app.domains.public_site.schema import BlogPostDetailOut, BlogPostSummaryOut, BlogTagOut


class PublicBlogRepositoryMixin:
    def list_blog_posts(self) -> list[BlogPostSummaryOut]:
        posts = self.session.scalars(
            self._public_blog_post_query()
            .options(
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
                selectinload(BlogPost.cover_image_file),
            )
            .order_by(BlogPost.published_at.desc().nullslast(), BlogPost.title.asc())
        ).all()
        return [self._map_blog_post_summary(post) for post in posts]

    def get_blog_post_by_slug(self, slug: str) -> BlogPostDetailOut | None:
        post = self.session.scalar(
            self._public_blog_post_query()
            .options(
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
                selectinload(BlogPost.cover_image_file),
            )
            .where(BlogPost.slug == slug)
        )
        if post is None:
            return None
        return self._map_blog_post_detail(post)

    def _list_featured_blog_posts(self, limit: int) -> list[BlogPostSummaryOut]:
        posts = self.session.scalars(
            self._public_blog_post_query()
            .options(
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
                selectinload(BlogPost.cover_image_file),
            )
            .order_by(BlogPost.is_featured.desc(), BlogPost.published_at.desc(), BlogPost.created_at.desc())
            .limit(limit)
        ).all()
        return [self._map_blog_post_summary(post) for post in posts]

    def _map_blog_post_summary(self, post: BlogPost) -> BlogPostSummaryOut:
        ordered_tag_links = sorted([link for link in post.tag_links if link.tag is not None], key=lambda item: item.tag.name.lower())
        return BlogPostSummaryOut(
            id=str(post.id),
            slug=post.slug,
            title=post.title,
            excerpt=post.excerpt,
            cover_image_file_id=str(post.cover_image_file_id) if post.cover_image_file_id else None,
            cover_image_alt=post.cover_image_alt,
            cover_image=self._map_media(post.cover_image_file, alt=post.cover_image_alt or post.title),
            reading_time_minutes=post.reading_time_minutes,
            status=post.status.value,
            is_featured=post.is_featured,
            published_at=post.published_at.isoformat() if post.published_at else None,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            tags=[BlogTagOut(id=str(link.tag.id), name=link.tag.name, slug=link.tag.slug) for link in ordered_tag_links],
        )

    def _map_blog_post_detail(self, post: BlogPost) -> BlogPostDetailOut:
        summary = self._map_blog_post_summary(post)
        return BlogPostDetailOut(
            **summary.model_dump(),
            content_markdown=post.content_markdown,
            seo_title=post.seo_title,
            seo_description=post.seo_description,
        )
