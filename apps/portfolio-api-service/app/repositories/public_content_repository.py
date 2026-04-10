from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import BlogPost, BlogPostTag, Profile, Project, ProjectSkill
from app.schemas.public import (
    BlogPostOut,
    BlogTagOut,
    ProfileOut,
    ProjectImageOut,
    ProjectOut,
    ProjectsListOut,
    SkillSummaryOut,
    SocialLinkOut,
)


class PublicContentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_profile(self) -> ProfileOut | None:
        profile = self.session.scalar(
            select(Profile)
            .options(selectinload(Profile.social_links))
            .where(Profile.is_public.is_(True))
            .order_by(Profile.updated_at.desc())
        )
        if profile is None:
            return None

        return ProfileOut.model_validate(
            {
                'id': str(profile.id),
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'headline': profile.headline,
                'short_intro': profile.short_intro,
                'long_bio': profile.long_bio,
                'location': profile.location,
                'email': profile.email,
                'phone': profile.phone,
                'avatar_file_id': str(profile.avatar_file_id) if profile.avatar_file_id else None,
                'hero_image_file_id': str(profile.hero_image_file_id) if profile.hero_image_file_id else None,
                'resume_file_id': str(profile.resume_file_id) if profile.resume_file_id else None,
                'cta_primary_label': profile.cta_primary_label,
                'cta_primary_url': profile.cta_primary_url,
                'cta_secondary_label': profile.cta_secondary_label,
                'cta_secondary_url': profile.cta_secondary_url,
                'is_public': profile.is_public,
                'social_links': [
                    SocialLinkOut.model_validate(
                        {
                            'id': str(link.id),
                            'profile_id': str(link.profile_id),
                            'platform': link.platform,
                            'label': link.label,
                            'url': link.url,
                            'icon_key': link.icon_key,
                            'sort_order': link.sort_order,
                            'is_visible': link.is_visible,
                        }
                    ).model_dump()
                    for link in profile.social_links
                ],
                'created_at': profile.created_at.isoformat(),
                'updated_at': profile.updated_at.isoformat(),
            }
        )

    def list_projects(self) -> list[ProjectOut]:
        projects = self.session.scalars(
            select(Project)
            .options(
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
                selectinload(Project.images),
            )
            .order_by(Project.sort_order.asc(), Project.title.asc())
        ).all()
        return [self._map_project(project) for project in projects]

    def list_blog_posts(self) -> list[BlogPostOut]:
        posts = self.session.scalars(
            select(BlogPost)
            .options(selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag))
            .order_by(BlogPost.published_at.desc().nullslast(), BlogPost.title.asc())
        ).all()
        return [self._map_blog_post(post) for post in posts]

    def get_blog_post_by_slug(self, slug: str) -> BlogPostOut | None:
        post = self.session.scalar(
            select(BlogPost)
            .options(selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag))
            .where(BlogPost.slug == slug)
        )
        if post is None:
            return None
        return self._map_blog_post(post)

    def _map_project(self, project: Project) -> ProjectOut:
        ordered_skill_links = sorted(
            [link for link in project.skill_links if link.skill is not None],
            key=lambda item: (item.skill.sort_order, item.skill.name.lower()),
        )
        ordered_images = sorted(project.images, key=lambda item: (item.sort_order, str(item.id)))

        return ProjectOut.model_validate(
            {
                'id': str(project.id),
                'slug': project.slug,
                'title': project.title,
                'teaser': project.teaser,
                'summary': project.summary,
                'description_markdown': project.description_markdown,
                'cover_image_file_id': str(project.cover_image_file_id) if project.cover_image_file_id else None,
                'github_url': project.github_url,
                'github_repo_owner': project.github_repo_owner,
                'github_repo_name': project.github_repo_name,
                'demo_url': project.demo_url,
                'company_name': project.company_name,
                'started_on': project.started_on.isoformat() if project.started_on else None,
                'ended_on': project.ended_on.isoformat() if project.ended_on else None,
                'duration_label': project.duration_label,
                'status': project.status,
                'state': project.state.value,
                'is_featured': project.is_featured,
                'sort_order': project.sort_order,
                'published_at': project.published_at.isoformat(),
                'created_at': project.created_at.isoformat(),
                'updated_at': project.updated_at.isoformat(),
                'skills': [
                    SkillSummaryOut.model_validate(
                        {
                            'id': str(link.skill.id),
                            'category_id': str(link.skill.category_id),
                            'name': link.skill.name,
                            'years_of_experience': link.skill.years_of_experience,
                            'icon_key': link.skill.icon_key,
                            'sort_order': link.skill.sort_order,
                            'is_highlighted': link.skill.is_highlighted,
                        }
                    ).model_dump()
                    for link in ordered_skill_links
                ],
                'images': [
                    ProjectImageOut.model_validate(
                        {
                            'id': str(image.id),
                            'project_id': str(image.project_id),
                            'image_file_id': str(image.image_file_id) if image.image_file_id else None,
                            'alt_text': image.alt_text,
                            'sort_order': image.sort_order,
                            'is_cover': image.is_cover,
                        }
                    ).model_dump()
                    for image in ordered_images
                ],
            }
        )

    def _map_blog_post(self, post: BlogPost) -> BlogPostOut:
        ordered_tag_links = sorted(
            [link for link in post.tag_links if link.tag is not None],
            key=lambda item: item.tag.name.lower(),
        )
        return BlogPostOut.model_validate(
            {
                'id': str(post.id),
                'slug': post.slug,
                'title': post.title,
                'excerpt': post.excerpt,
                'content_markdown': post.content_markdown,
                'cover_image_file_id': str(post.cover_image_file_id) if post.cover_image_file_id else None,
                'cover_image_alt': post.cover_image_alt,
                'reading_time_minutes': post.reading_time_minutes,
                'status': post.status.value,
                'is_featured': post.is_featured,
                'published_at': post.published_at.isoformat() if post.published_at else None,
                'seo_title': post.seo_title,
                'seo_description': post.seo_description,
                'created_at': post.created_at.isoformat(),
                'updated_at': post.updated_at.isoformat(),
                'tags': [
                    BlogTagOut.model_validate(
                        {
                            'id': str(link.tag.id),
                            'name': link.tag.name,
                            'slug': link.tag.slug,
                        }
                    ).model_dump()
                    for link in ordered_tag_links
                ],
            }
        )
