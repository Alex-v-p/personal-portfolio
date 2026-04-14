from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import NavigationItem, Profile, Skill, SkillCategory
from app.domains.public_site.schema import ContactMethodOut, ExpertiseGroupOut, NavigationItemOut, NavigationListOut, ProfileOut, SocialLinkOut, SiteShellOut


class PublicProfileRepositoryMixin:
    def get_profile(self) -> ProfileOut | None:
        profile = self._get_profile_record()
        if profile is None:
            return None
        return self._map_profile(profile)

    def list_navigation(self) -> list[NavigationItemOut]:
        items = self.session.scalars(
            select(NavigationItem)
            .where(NavigationItem.is_visible.is_(True))
            .order_by(NavigationItem.sort_order.asc(), NavigationItem.label.asc())
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
            groups.append(ExpertiseGroupOut(title=category.name, tags=[skill.name for skill in ordered_skills]))
        return groups

    def _get_highlighted_skill_names(self) -> list[str]:
        skills = self.session.scalars(
            select(Skill).where(Skill.is_highlighted.is_(True)).order_by(Skill.sort_order.asc(), Skill.name.asc())
        ).all()
        if skills:
            return [skill.name for skill in skills]
        fallback = self.session.scalars(select(Skill).order_by(Skill.sort_order.asc(), Skill.name.asc())).all()
        return [skill.name for skill in fallback[:6]]

    def _map_profile(self, profile: Profile) -> ProfileOut:
        intro_paragraphs = [part for part in [profile.short_intro, profile.long_bio] if part]
        expertise_groups = self._get_expertise_groups()
        resume_url = self.media_resolver.resolve(profile.resume_file)
        primary_cta_url = profile.cta_primary_url
        if primary_cta_url == 'media://resume' or (primary_cta_url and primary_cta_url.startswith('/assets/')):
            primary_cta_url = resume_url
        elif not primary_cta_url and resume_url:
            primary_cta_url = resume_url
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
            cta_primary_url=primary_cta_url,
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
