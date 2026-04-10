from __future__ import annotations

from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.data.public_content import BLOG_POSTS, PROFILE, PROJECTS
from app.db.models import BlogPost, BlogPostTag, Profile, Project, ProjectSkill, SkillCategory
from app.schemas.public import BlogPostOut, ProfileOut, ProjectLinkOut, ProjectOut


class PublicContentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_profile(self) -> ProfileOut:
        profile = self.session.scalar(
            select(Profile)
            .options(selectinload(Profile.social_links))
            .where(Profile.is_public.is_(True))
            .order_by(Profile.updated_at.desc())
        )
        if profile is None:
            return ProfileOut.model_validate(PROFILE)

        skill_categories = self.session.scalars(
            select(SkillCategory)
            .options(selectinload(SkillCategory.skills))
            .order_by(SkillCategory.sort_order.asc(), SkillCategory.name.asc())
        ).all()
        expertise_groups: list[dict] = []
        highlighted_skills: list[str] = []
        for category in skill_categories:
            ordered_skills = sorted(category.skills, key=lambda item: (item.sort_order, item.name.lower()))
            skill_names = [skill.name for skill in ordered_skills]
            if skill_names:
                expertise_groups.append({'title': category.name, 'tags': skill_names})
            highlighted_skills.extend(skill.name for skill in ordered_skills if skill.is_highlighted)

        hero_actions: list[dict] = []
        if profile.cta_primary_label and profile.cta_primary_url:
            hero_actions.append(
                {
                    'label': profile.cta_primary_label,
                    'appearance': 'secondary',
                    'href': profile.cta_primary_url,
                    'open_in_new_tab': False,
                }
            )
        if profile.cta_secondary_label and profile.cta_secondary_url:
            hero_actions.append(
                {
                    'label': profile.cta_secondary_label,
                    'appearance': 'primary',
                    'router_link': profile.cta_secondary_url,
                    'open_in_new_tab': False,
                }
            )

        intro_paragraphs = [profile.short_intro]
        if profile.long_bio and profile.long_bio != profile.short_intro:
            intro_paragraphs.append(profile.long_bio)

        return ProfileOut.model_validate(
            {
                'id': str(profile.id),
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'name': f'{profile.first_name} {profile.last_name}'.strip(),
                'headline': profile.headline,
                'role': profile.headline,
                'greeting': f"Hi, I'm {profile.first_name}",
                'location': profile.location or '',
                'email': profile.email or '',
                'phone': profile.phone or '',
                'short_intro': profile.short_intro,
                'long_bio': profile.long_bio or profile.short_intro,
                'hero_title': f"I'm a {profile.headline}",
                'summary': profile.short_intro,
                'short_bio': profile.short_intro,
                'footer_description': profile.long_bio or profile.short_intro,
                'avatar_file_id': str(profile.avatar_file_id) if profile.avatar_file_id else None,
                'hero_image_file_id': str(profile.hero_image_file_id) if profile.hero_image_file_id else None,
                'resume_file_id': str(profile.resume_file_id) if profile.resume_file_id else None,
                'avatar_url': None,
                'hero_image_url': None,
                'resume_url': profile.cta_primary_url,
                'skills': highlighted_skills[:6],
                'expertise_groups': expertise_groups,
                'intro_paragraphs': intro_paragraphs,
                'availability': [],
                'hero_actions': hero_actions,
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
        if not projects:
            return [ProjectOut.model_validate(project) for project in PROJECTS]
        return [self._map_project(project) for project in projects]

    def list_blog_posts(self) -> list[BlogPostOut]:
        posts = self.session.scalars(
            select(BlogPost)
            .options(selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag))
            .order_by(BlogPost.published_at.desc().nullslast(), BlogPost.title.asc())
        ).all()
        if not posts:
            return [BlogPostOut.model_validate(post) for post in BLOG_POSTS]
        return [self._map_blog_post(post) for post in posts]

    def get_blog_post_by_slug(self, slug: str) -> BlogPostOut | None:
        post = self.session.scalar(
            select(BlogPost)
            .options(selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag))
            .where(BlogPost.slug == slug)
        )
        if post is not None:
            return self._map_blog_post(post)

        for fallback_post in BLOG_POSTS:
            if fallback_post['slug'] == slug:
                return BlogPostOut.model_validate(fallback_post)
        return None

    def _map_project(self, project: Project) -> ProjectOut:
        ordered_tags = [link.skill.name for link in sorted(project.skill_links, key=lambda item: (item.skill.sort_order, item.skill.name.lower()))]
        cover_image = next((image for image in project.images if image.is_cover), None)
        links: list[ProjectLinkOut] = []
        if project.github_url:
            links.append(ProjectLinkOut(label='GitHub README', href=project.github_url))
        if project.demo_url:
            links.append(ProjectLinkOut(label='Live Demo', href=project.demo_url))
        links.append(ProjectLinkOut(label='Read More', router_link=['/projects']))
        return ProjectOut.model_validate(
            {
                'id': str(project.id),
                'slug': project.slug,
                'title': project.title,
                'teaser': project.teaser,
                'short_description': project.teaser,
                'summary': project.summary or project.teaser,
                'description_markdown': project.description_markdown,
                'organization': project.company_name or 'Personal project',
                'duration': project.duration_label,
                'duration_label': project.duration_label,
                'status': project.status,
                'state': project.state.value,
                'category': self._infer_project_category(ordered_tags),
                'tags': ordered_tags,
                'featured': project.is_featured,
                'is_featured': project.is_featured,
                'image_alt': cover_image.alt_text if cover_image and cover_image.alt_text else project.title,
                'cover_image_alt': cover_image.alt_text if cover_image and cover_image.alt_text else project.title,
                'cover_image_file_id': str(project.cover_image_file_id) if project.cover_image_file_id else None,
                'cover_image_url': None,
                'highlight': project.summary or project.teaser,
                'github_url': project.github_url,
                'github_repo_name': project.github_repo_name,
                'demo_url': project.demo_url,
                'started_on': project.started_on.isoformat() if project.started_on else None,
                'ended_on': project.ended_on.isoformat() if project.ended_on else None,
                'published_at': project.published_at.date().isoformat(),
                'sort_order': project.sort_order,
                'links': [link.model_dump() for link in links],
            }
        )

    def _map_blog_post(self, post: BlogPost) -> BlogPostOut:
        tags = [link.tag.name for link in sorted(post.tag_links, key=lambda item: item.tag.name.lower())]
        return BlogPostOut.model_validate(
            {
                'id': str(post.id),
                'slug': post.slug,
                'title': post.title,
                'excerpt': post.excerpt,
                'published_at': post.published_at.date().isoformat() if post.published_at else '',
                'read_time': self._build_read_time(post.reading_time_minutes),
                'reading_time_minutes': post.reading_time_minutes or 0,
                'category': tags[0] if tags else 'Blog',
                'tags': tags,
                'featured': post.is_featured,
                'is_featured': post.is_featured,
                'cover_alt': post.cover_image_alt or post.title,
                'cover_image_alt': post.cover_image_alt or post.title,
                'cover_image_file_id': str(post.cover_image_file_id) if post.cover_image_file_id else None,
                'cover_image_url': None,
                'status': post.status.value,
                'content_markdown': post.content_markdown,
                'seo_title': post.seo_title,
                'seo_description': post.seo_description,
            }
        )

    @staticmethod
    def _build_read_time(minutes: int | None) -> str:
        value = minutes or 0
        return f'{value} min read'

    @staticmethod
    def _infer_project_category(tags: list[str]) -> str:
        if not tags:
            return 'Project'
        category_lookup = defaultdict(
            lambda: 'Project',
            {
                'Angular': 'Frontend',
                'Tailwind CSS': 'Frontend',
                'TypeScript': 'Frontend',
                'React': 'Frontend',
                'Laravel': 'Backend',
                '.NET': 'Backend',
                'REST APIs': 'Backend',
                'Spring Boot': 'Backend',
                'Python': 'AI & Data',
                'TensorFlow': 'AI & Data',
                'EfficientNet': 'AI & Data',
                'ML': 'AI & Data',
            },
        )
        return category_lookup[tags[0]]
