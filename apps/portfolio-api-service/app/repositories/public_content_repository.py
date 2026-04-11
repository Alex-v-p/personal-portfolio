from __future__ import annotations

from collections import defaultdict
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.db.models import (
    BlogPost,
    BlogPostTag,
    Experience,
    ExperienceSkill,
    GithubSnapshot,
    MediaFile,
    NavigationItem,
    Profile,
    Project,
    ProjectImage,
    ProjectSkill,
    Skill,
    SkillCategory,
)
from app.schemas.public import (
    BlogPostOut,
    BlogTagOut,
    ContactMethodOut,
    ExperienceOut,
    ExpertiseGroupOut,
    GithubContributionDayOut,
    GithubSnapshotOut,
    HomeOut,
    NavigationItemOut,
    NavigationListOut,
    ProfileOut,
    ProjectImageOut,
    ProjectOut,
    PublicMediaAssetOut,
    SkillSummaryOut,
    SiteShellOut,
    SocialLinkOut,
    StatItemOut,
    StatsOut,
)
from app.services.media_resolver import PublicMediaUrlResolver


class PublicContentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.media_resolver = PublicMediaUrlResolver()

    def get_profile(self) -> ProfileOut | None:
        profile = self._get_profile_record()
        if profile is None:
            return None
        return self._map_profile(profile)

    def list_navigation(self) -> list[NavigationItemOut]:
        items = self.session.scalars(
            select(NavigationItem).where(NavigationItem.is_visible.is_(True)).order_by(NavigationItem.sort_order.asc(), NavigationItem.label.asc())
        ).all()
        return [
            NavigationItemOut(
                id=str(item.id),
                label=item.label,
                route_path=item.route_path,
                is_external=item.is_external,
                sort_order=item.sort_order,
                is_visible=item.is_visible,
            )
            for item in items
        ]

    def get_site_shell(self) -> SiteShellOut | None:
        profile = self.get_profile()
        if profile is None:
            return None
        navigation_items = self.list_navigation()
        return SiteShellOut(
            navigation=NavigationListOut(items=navigation_items, total=len(navigation_items)),
            profile=profile,
            footer_text=profile.footer_description,
            contact_methods=self._build_contact_methods(profile),
        )

    def get_home(self) -> HomeOut | None:
        profile = self.get_profile()
        if profile is None:
            return None
        projects = self.list_projects()
        blog_posts = self.list_blog_posts()
        experience = self.list_experience()
        return HomeOut(
            hero=profile,
            featured_projects=[project for project in projects if project.is_featured][:2] or projects[:2],
            featured_blog_posts=[post for post in blog_posts if post.is_featured][:2] or blog_posts[:2],
            expertise_groups=profile.expertise_groups,
            experience_preview=experience[:3],
            contact_preview=self._build_contact_methods(profile)[:4],
        )

    def list_projects(self) -> list[ProjectOut]:
        projects = self.session.scalars(
            select(Project)
            .options(
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
                selectinload(Project.images).selectinload(ProjectImage.image_file),
                selectinload(Project.cover_image_file),
            )
            .order_by(Project.sort_order.asc(), Project.title.asc())
        ).all()
        return [self._map_project(project) for project in projects]

    def get_project_by_slug(self, slug: str) -> ProjectOut | None:
        project = self.session.scalar(
            select(Project)
            .options(
                selectinload(Project.skill_links).selectinload(ProjectSkill.skill),
                selectinload(Project.images).selectinload(ProjectImage.image_file),
                selectinload(Project.cover_image_file),
            )
            .where(Project.slug == slug)
        )
        if project is None:
            return None
        return self._map_project(project)

    def list_blog_posts(self) -> list[BlogPostOut]:
        posts = self.session.scalars(
            select(BlogPost)
            .options(
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
                selectinload(BlogPost.cover_image_file),
            )
            .order_by(BlogPost.published_at.desc().nullslast(), BlogPost.title.asc())
        ).all()
        return [self._map_blog_post(post) for post in posts]

    def get_blog_post_by_slug(self, slug: str) -> BlogPostOut | None:
        post = self.session.scalar(
            select(BlogPost)
            .options(
                selectinload(BlogPost.tag_links).selectinload(BlogPostTag.tag),
                selectinload(BlogPost.cover_image_file),
            )
            .where(BlogPost.slug == slug)
        )
        if post is None:
            return None
        return self._map_blog_post(post)

    def list_experience(self) -> list[ExperienceOut]:
        items = self.session.scalars(
            select(Experience)
            .options(
                selectinload(Experience.skill_links).selectinload(ExperienceSkill.skill),
                selectinload(Experience.logo_file),
            )
            .order_by(Experience.sort_order.asc(), Experience.start_date.desc())
        ).all()
        return [self._map_experience(item) for item in items]

    def get_latest_github_snapshot(self) -> GithubSnapshotOut | None:
        snapshot = self.session.scalar(
            select(GithubSnapshot)
            .options(selectinload(GithubSnapshot.contribution_days))
            .order_by(GithubSnapshot.snapshot_date.desc(), GithubSnapshot.created_at.desc())
        )
        if snapshot is None:
            return None
        return self._map_github_snapshot(snapshot)

    def get_stats(self) -> StatsOut:
        project_count = self.session.scalar(select(func.count(Project.id))) or 0
        blog_count = self.session.scalar(select(func.count(BlogPost.id))) or 0
        skill_count = self.session.scalar(select(func.count(Skill.id))) or 0
        featured_project_count = self.session.scalar(select(func.count(Project.id)).where(Project.is_featured.is_(True))) or 0
        featured_blog_count = self.session.scalar(select(func.count(BlogPost.id)).where(BlogPost.is_featured.is_(True))) or 0
        experience_count = self.session.scalar(select(func.count(Experience.id))) or 0
        snapshot = self.get_latest_github_snapshot()
        contribution_weeks = self._build_contribution_weeks(snapshot.contribution_days if snapshot else [])
        return StatsOut(
            contribution_weeks=contribution_weeks,
            github_summary=StatItemOut(
                id='github-total-commits',
                label='GitHub activity',
                value=str(snapshot.total_commits if snapshot and snapshot.total_commits is not None else 0),
                description='Seeded GitHub snapshot total commits currently available for the public stats page.',
                meta=f"{snapshot.username} · latest snapshot" if snapshot else 'No snapshot available',
                footnote=f"{snapshot.public_repo_count} public repositories" if snapshot else 'Seed GitHub data not available',
            ),
            latest_github_snapshot=snapshot,
            portfolio_highlights=[
                StatItemOut(
                    id='highlight-featured-projects',
                    label='Featured projects',
                    value=str(featured_project_count),
                    description='Projects currently marked as featured in the portfolio database.',
                ),
                StatItemOut(
                    id='highlight-featured-posts',
                    label='Featured posts',
                    value=str(featured_blog_count),
                    description='Blog posts highlighted for the home page and discovery flow.',
                ),
            ],
            portfolio_stats=[
                StatItemOut(id='stat-projects', label='Projects', value=str(project_count), description='Published portfolio projects.'),
                StatItemOut(id='stat-posts', label='Blog posts', value=str(blog_count), description='Posts available on the public blog.'),
                StatItemOut(id='stat-skills', label='Skills', value=str(skill_count), description='Skills currently modeled in the database.'),
                StatItemOut(id='stat-experience', label='Experience entries', value=str(experience_count), description='Experience timeline rows available publicly.'),
            ],
            month_labels=self._build_month_labels(snapshot.contribution_days if snapshot else []),
            weekday_labels=['Mon', '', 'Wed', '', 'Fri', '', ''],
        )

    def _get_profile_record(self) -> Profile | None:
        return self.session.scalar(
            select(Profile)
            .options(
                selectinload(Profile.social_links),
                selectinload(Profile.avatar_file),
                selectinload(Profile.hero_image_file),
                selectinload(Profile.resume_file),
            )
            .where(Profile.is_public.is_(True))
            .order_by(Profile.updated_at.desc())
        )

    def _get_expertise_groups(self) -> list[ExpertiseGroupOut]:
        categories = self.session.scalars(
            select(SkillCategory)
            .options(selectinload(SkillCategory.skills))
            .order_by(SkillCategory.sort_order.asc(), SkillCategory.name.asc())
        ).all()
        groups: list[ExpertiseGroupOut] = []
        for category in categories:
            ordered_skills = sorted(category.skills, key=lambda skill: (skill.sort_order, skill.name.lower()))
            if not ordered_skills:
                continue
            groups.append(
                ExpertiseGroupOut(
                    title=category.name,
                    tags=[skill.name for skill in ordered_skills],
                )
            )
        return groups

    def _map_profile(self, profile: Profile) -> ProfileOut:
        intro_paragraphs = [part for part in [profile.short_intro, profile.long_bio] if part]
        expertise_groups = self._get_expertise_groups()
        return ProfileOut(
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
                SocialLinkOut(
                    id=str(link.id),
                    profile_id=str(link.profile_id),
                    platform=link.platform,
                    label=link.label,
                    url=link.url,
                    icon_key=link.icon_key,
                    sort_order=link.sort_order,
                    is_visible=link.is_visible,
                )
                for link in sorted(profile.social_links, key=lambda item: (item.sort_order, item.label.lower()))
                if link.is_visible
            ],
            footer_description=profile.long_bio or profile.short_intro,
            intro_paragraphs=intro_paragraphs,
            availability=['Open to internships', 'Remote friendly', 'Portfolio projects'],
            skills=self._get_highlighted_skill_names(),
            expertise_groups=expertise_groups,
            created_at=profile.created_at.isoformat(),
            updated_at=profile.updated_at.isoformat(),
        )

    def _get_highlighted_skill_names(self) -> list[str]:
        skills = self.session.scalars(
            select(Skill).where(Skill.is_highlighted.is_(True)).order_by(Skill.sort_order.asc(), Skill.name.asc())
        ).all()
        if skills:
            return [skill.name for skill in skills]
        fallback = self.session.scalars(select(Skill).order_by(Skill.sort_order.asc(), Skill.name.asc())).all()
        return [skill.name for skill in fallback[:6]]

    def _map_media(self, media_file: MediaFile | None, alt: str | None = None) -> PublicMediaAssetOut | None:
        url = self.media_resolver.resolve(media_file)
        if media_file is None or url is None:
            return None
        return PublicMediaAssetOut(
            id=str(media_file.id),
            url=url,
            alt=alt or media_file.alt_text,
            file_name=media_file.original_filename,
            mime_type=media_file.mime_type,
            width=None,
            height=None,
        )

    def _map_project(self, project: Project) -> ProjectOut:
        ordered_skill_links = sorted(
            [link for link in project.skill_links if link.skill is not None],
            key=lambda item: (item.skill.sort_order, item.skill.name.lower()),
        )
        ordered_images = sorted(project.images, key=lambda item: (item.sort_order, str(item.id)))
        return ProjectOut(
            id=str(project.id),
            slug=project.slug,
            title=project.title,
            teaser=project.teaser,
            summary=project.summary,
            description_markdown=project.description_markdown,
            cover_image_file_id=str(project.cover_image_file_id) if project.cover_image_file_id else None,
            cover_image=self._map_media(project.cover_image_file, alt=project.title),
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
            skills=[
                SkillSummaryOut(
                    id=str(link.skill.id),
                    category_id=str(link.skill.category_id),
                    name=link.skill.name,
                    years_of_experience=link.skill.years_of_experience,
                    icon_key=link.skill.icon_key,
                    sort_order=link.skill.sort_order,
                    is_highlighted=link.skill.is_highlighted,
                )
                for link in ordered_skill_links
            ],
            images=[
                ProjectImageOut(
                    id=str(image.id),
                    project_id=str(image.project_id),
                    image_file_id=str(image.image_file_id) if image.image_file_id else None,
                    alt_text=image.alt_text,
                    sort_order=image.sort_order,
                    is_cover=image.is_cover,
                    image=self._map_media(image.image_file, alt=image.alt_text or project.title),
                )
                for image in ordered_images
            ],
        )

    def _map_blog_post(self, post: BlogPost) -> BlogPostOut:
        ordered_tag_links = sorted([link for link in post.tag_links if link.tag is not None], key=lambda item: item.tag.name.lower())
        return BlogPostOut(
            id=str(post.id),
            slug=post.slug,
            title=post.title,
            excerpt=post.excerpt,
            content_markdown=post.content_markdown,
            cover_image_file_id=str(post.cover_image_file_id) if post.cover_image_file_id else None,
            cover_image_alt=post.cover_image_alt,
            cover_image=self._map_media(post.cover_image_file, alt=post.cover_image_alt or post.title),
            reading_time_minutes=post.reading_time_minutes,
            status=post.status.value,
            is_featured=post.is_featured,
            published_at=post.published_at.isoformat() if post.published_at else None,
            seo_title=post.seo_title,
            seo_description=post.seo_description,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            tags=[BlogTagOut(id=str(link.tag.id), name=link.tag.name, slug=link.tag.slug) for link in ordered_tag_links],
        )

    def _map_experience(self, item: Experience) -> ExperienceOut:
        ordered_skills = sorted([link.skill.name for link in item.skill_links if link.skill is not None])
        return ExperienceOut(
            id=str(item.id),
            organization_name=item.organization_name,
            role_title=item.role_title,
            location=item.location,
            experience_type=item.experience_type,
            start_date=item.start_date.isoformat(),
            end_date=item.end_date.isoformat() if item.end_date else None,
            is_current=item.is_current,
            summary=item.summary,
            description_markdown=item.description_markdown,
            logo_file_id=str(item.logo_file_id) if item.logo_file_id else None,
            logo=self._map_media(item.logo_file, alt=item.organization_name),
            sort_order=item.sort_order,
            skill_names=ordered_skills,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat(),
        )

    def _map_github_snapshot(self, snapshot: GithubSnapshot) -> GithubSnapshotOut:
        ordered_days = sorted(snapshot.contribution_days, key=lambda item: item.contribution_date)
        return GithubSnapshotOut(
            id=str(snapshot.id),
            snapshot_date=snapshot.snapshot_date.isoformat(),
            username=snapshot.username,
            public_repo_count=snapshot.public_repo_count,
            followers_count=snapshot.followers_count,
            following_count=snapshot.following_count,
            total_stars=snapshot.total_stars,
            total_commits=snapshot.total_commits,
            created_at=snapshot.created_at.isoformat(),
            contribution_days=[
                GithubContributionDayOut(
                    date=day.contribution_date.isoformat(),
                    count=day.contribution_count,
                    level=day.level,
                )
                for day in ordered_days
            ],
        )

    def _build_contact_methods(self, profile: ProfileOut) -> list[ContactMethodOut]:
        methods: list[ContactMethodOut] = []
        if profile.email:
            methods.append(ContactMethodOut(
                id='contact-email',
                platform='email',
                label='Email',
                value=profile.email,
                href=f'mailto:{profile.email}',
                action_label='Send Email',
                icon_key='mail',
                description='Best for project enquiries, internships, and collaboration.',
                sort_order=1,
                is_visible=True,
            ))
        if profile.phone:
            methods.append(ContactMethodOut(
                id='contact-phone',
                platform='phone',
                label='Phone',
                value=profile.phone,
                href=f"tel:{profile.phone.replace(' ', '')}",
                action_label='Call',
                icon_key='phone',
                description='Useful for quick coordination or planning a meeting.',
                sort_order=2,
                is_visible=True,
            ))
        for link in profile.social_links:
            methods.append(ContactMethodOut(
                id=f'contact-{link.platform}',
                platform=link.platform,
                label=link.label,
                value=link.url.replace('https://', '').replace('http://', ''),
                href=link.url,
                action_label='Connect +' if link.platform in {'github', 'linkedin'} else 'Open',
                icon_key=link.icon_key,
                description='Code samples, experiments, and project work.' if link.platform == 'github' else (
                    'Professional background and experience.' if link.platform == 'linkedin' else 'Direct line for portfolio contact.'
                ),
                sort_order=(link.sort_order or 0) + 10,
                is_visible=link.is_visible,
            ))
        if profile.location:
            methods.append(ContactMethodOut(
                id='contact-location',
                platform='location',
                label='Location',
                value=profile.location,
                href=f'https://maps.google.com/?q={profile.location}',
                action_label='View Map',
                icon_key='map-pin',
                description='Available for on-site, hybrid, or remote collaboration.',
                sort_order=99,
                is_visible=True,
            ))
        return sorted([method for method in methods if method.is_visible], key=lambda item: (item.sort_order, item.label.lower()))

    def _build_contribution_weeks(self, days: list[GithubContributionDayOut]) -> list[list[int]]:
        if not days:
            return [[0] * 7 for _ in range(12)]
        grouped: dict[date, int] = {date.fromisoformat(day.date): day.level for day in days}
        ordered_dates = sorted(grouped)
        first = ordered_dates[0]
        start = first
        while start.weekday() != 0:
            start = date.fromordinal(start.toordinal() - 1)
        end = ordered_dates[-1]
        while end.weekday() != 6:
            end = date.fromordinal(end.toordinal() + 1)
        weeks: list[list[int]] = []
        current = start
        while current <= end:
            week: list[int] = []
            for _ in range(7):
                week.append(grouped.get(current, 0))
                current = date.fromordinal(current.toordinal() + 1)
            weeks.append(week)
        return weeks

    def _build_month_labels(self, days: list[GithubContributionDayOut]) -> list[str]:
        if not days:
            return [''] * 12
        grouped: dict[date, int] = {date.fromisoformat(day.date): day.level for day in days}
        ordered_dates = sorted(grouped)
        start = ordered_dates[0]
        while start.weekday() != 0:
            start = date.fromordinal(start.toordinal() - 1)
        end = ordered_dates[-1]
        while end.weekday() != 6:
            end = date.fromordinal(end.toordinal() + 1)
        labels: list[str] = []
        current = start
        last_month = None
        while current <= end:
            labels.append(current.strftime('%b') if current.month != last_month else '')
            last_month = current.month
            current = date.fromordinal(current.toordinal() + 7)
        return labels
