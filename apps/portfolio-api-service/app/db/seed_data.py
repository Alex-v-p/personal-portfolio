from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.seed_content import (
    BLOG_POST_ROWS,
    BLOG_TAG_NAMES_BY_POST_SLUG,
    PROFILE_ROW,
    PROJECT_ROWS,
    PROJECT_SKILL_NAMES_BY_PROJECT_SLUG,
)
from app.data.seed_ids import seed_uuid
from app.db.models import (
    BlogPost,
    BlogPostTag,
    BlogTag,
    Experience,
    ExperienceSkill,
    GithubContributionDay,
    GithubSnapshot,
    MediaFile,
    MediaVisibility,
    NavigationItem,
    Profile,
    Project,
    ProjectImage,
    ProjectSkill,
    ProjectState,
    PublicationStatus,
    Skill,
    SkillCategory,
    SocialLink,
)

NAVIGATION_ITEMS = [
    {'id': 'nav-home', 'label': 'Home', 'route_path': '/', 'is_external': False, 'sort_order': 1, 'is_visible': True},
    {'id': 'nav-projects', 'label': 'Projects', 'route_path': '/projects', 'is_external': False, 'sort_order': 2, 'is_visible': True},
    {'id': 'nav-blog', 'label': 'Blog', 'route_path': '/blog', 'is_external': False, 'sort_order': 3, 'is_visible': True},
    {'id': 'nav-contact', 'label': 'Contact', 'route_path': '/contact', 'is_external': False, 'sort_order': 4, 'is_visible': True},
    {'id': 'nav-stats', 'label': 'Stats', 'route_path': '/stats', 'is_external': False, 'sort_order': 5, 'is_visible': True},
    {'id': 'nav-assistant', 'label': 'Assistant', 'route_path': '/assistant', 'is_external': False, 'sort_order': 6, 'is_visible': False},
]

TIMESTAMP = datetime(2025, 10, 1, 9, 0, tzinfo=UTC)

MEDIA_FILES = [
    {
        'id': 'file-avatar-alex',
        'bucket_name': 'portfolio',
        'object_key': 'profiles/alex/avatar.png',
        'original_filename': 'alex-avatar.png',
        'stored_filename': 'alex-avatar-1.png',
        'mime_type': 'image/png',
        'file_size_bytes': 248130,
        'checksum': 'sha256-avatar-alex',
        'public_url': '/assets/mock/profile-avatar.png',
        'alt_text': 'Portrait placeholder for Alex van Poppel',
        'title': 'Profile avatar',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-hero-portrait',
        'bucket_name': 'portfolio',
        'object_key': 'profiles/alex/hero.png',
        'original_filename': 'hero.png',
        'stored_filename': 'hero-1.png',
        'mime_type': 'image/png',
        'file_size_bytes': 612004,
        'checksum': 'sha256-hero-alex',
        'public_url': '/assets/mock/hero-image.png',
        'alt_text': 'Hero image placeholder for the portfolio',
        'title': 'Hero image',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-resume',
        'bucket_name': 'portfolio',
        'object_key': 'profiles/alex/resume.pdf',
        'original_filename': 'alex-van-poppel-resume.pdf',
        'stored_filename': 'resume-2025.pdf',
        'mime_type': 'application/pdf',
        'file_size_bytes': 152320,
        'checksum': 'sha256-resume-alex',
        'public_url': '/assets/mock-resume.pdf',
        'title': 'Resume',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-project-portfolio-cover',
        'bucket_name': 'portfolio',
        'object_key': 'projects/personal-portfolio/cover.png',
        'original_filename': 'personal-portfolio-cover.png',
        'stored_filename': 'project-cover-portfolio.png',
        'mime_type': 'image/png',
        'file_size_bytes': 480221,
        'checksum': 'sha256-project-portfolio-cover',
        'public_url': '/assets/mock/projects/personal-portfolio-cover.png',
        'alt_text': 'Wireframe-inspired portfolio layout mock-up',
        'title': 'Portfolio project cover image',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-project-plant-cover',
        'bucket_name': 'portfolio',
        'object_key': 'projects/plant-care-app/cover.png',
        'original_filename': 'plant-care-cover.png',
        'stored_filename': 'project-cover-plant.png',
        'mime_type': 'image/png',
        'file_size_bytes': 390110,
        'checksum': 'sha256-project-plant-cover',
        'public_url': '/assets/mock/projects/plant-care-cover.png',
        'alt_text': 'Plant care dashboard concept',
        'title': 'Plant care project cover',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-project-motogp-cover',
        'bucket_name': 'portfolio',
        'object_key': 'projects/motogp-ticketing/cover.png',
        'original_filename': 'motogp-cover.png',
        'stored_filename': 'project-cover-motogp.png',
        'mime_type': 'image/png',
        'file_size_bytes': 400235,
        'checksum': 'sha256-project-motogp-cover',
        'public_url': '/assets/mock/projects/motogp-cover.png',
        'alt_text': 'MotoGP booking interface mock-up',
        'title': 'MotoGP project cover',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-project-dino-cover',
        'bucket_name': 'portfolio',
        'object_key': 'projects/dino-classifier/cover.png',
        'original_filename': 'dino-cover.png',
        'stored_filename': 'project-cover-dino.png',
        'mime_type': 'image/png',
        'file_size_bytes': 360421,
        'checksum': 'sha256-project-dino-cover',
        'public_url': '/assets/mock/projects/dino-cover.png',
        'alt_text': 'Dataset and model-training workflow diagram',
        'title': 'Dinosaur classifier cover',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-project-auction-cover',
        'bucket_name': 'portfolio',
        'object_key': 'projects/auction-house-api/cover.png',
        'original_filename': 'auction-cover.png',
        'stored_filename': 'project-cover-auction.png',
        'mime_type': 'image/png',
        'file_size_bytes': 342111,
        'checksum': 'sha256-project-auction-cover',
        'public_url': '/assets/mock/projects/auction-cover.png',
        'alt_text': 'Auction workflow and service architecture sketch',
        'title': 'Auction API cover',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-blog-shell-cover',
        'bucket_name': 'portfolio',
        'object_key': 'blog/building-a-portfolio-shell/cover.png',
        'original_filename': 'portfolio-shell-cover.png',
        'stored_filename': 'blog-shell-cover.png',
        'mime_type': 'image/png',
        'file_size_bytes': 320811,
        'checksum': 'sha256-blog-shell-cover',
        'public_url': '/assets/mock/blog/portfolio-shell-cover.png',
        'alt_text': 'Portfolio shell layout illustration',
        'title': 'Portfolio shell article cover',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-blog-mock-data-cover',
        'bucket_name': 'portfolio',
        'object_key': 'blog/mock-data-first/cover.png',
        'original_filename': 'mock-data-cover.png',
        'stored_filename': 'blog-mock-data-cover.png',
        'mime_type': 'image/png',
        'file_size_bytes': 312213,
        'checksum': 'sha256-blog-mock-data-cover',
        'public_url': '/assets/mock/blog/mock-data-cover.png',
        'alt_text': 'Mock data objects represented as cards',
        'title': 'Mock data article cover',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-blog-storytelling-cover',
        'bucket_name': 'portfolio',
        'object_key': 'blog/student-projects-and-storytelling/cover.png',
        'original_filename': 'storytelling-cover.png',
        'stored_filename': 'blog-storytelling-cover.png',
        'mime_type': 'image/png',
        'file_size_bytes': 315773,
        'checksum': 'sha256-blog-storytelling-cover',
        'public_url': '/assets/mock/blog/storytelling-cover.png',
        'alt_text': 'Cards representing project storytelling',
        'title': 'Storytelling article cover',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'file-blog-components-cover',
        'bucket_name': 'portfolio',
        'object_key': 'blog/components-before-polish/cover.png',
        'original_filename': 'components-cover.png',
        'stored_filename': 'blog-components-cover.png',
        'mime_type': 'image/png',
        'file_size_bytes': 302921,
        'checksum': 'sha256-blog-components-cover',
        'public_url': '/assets/mock/blog/components-cover.png',
        'alt_text': 'UI components arranged in a grid',
        'title': 'Components article cover',
        'visibility': MediaVisibility.PUBLIC,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
]

SOCIAL_LINKS = [
    {
        'id': 'social-github',
        'profile_id': PROFILE_ROW['id'],
        'platform': 'github',
        'label': 'GitHub',
        'url': 'https://github.com/shuzu',
        'icon_key': 'github',
        'sort_order': 1,
        'is_visible': True,
    },
    {
        'id': 'social-linkedin',
        'profile_id': PROFILE_ROW['id'],
        'platform': 'linkedin',
        'label': 'LinkedIn',
        'url': 'https://linkedin.com/in/alex-van-poppel',
        'icon_key': 'linkedin',
        'sort_order': 2,
        'is_visible': True,
    },
    {
        'id': 'social-email',
        'profile_id': PROFILE_ROW['id'],
        'platform': 'email',
        'label': 'Email',
        'url': 'mailto:hello@shuzu.dev',
        'icon_key': 'mail',
        'sort_order': 3,
        'is_visible': True,
    },
]

SKILL_CATEGORIES = [
    {'id': 'cat-frontend', 'name': 'Front-End', 'description': 'UI and client-side technologies', 'sort_order': 1},
    {'id': 'cat-backend', 'name': 'Back-End', 'description': 'API and server-side development', 'sort_order': 2},
    {'id': 'cat-ai', 'name': 'AI', 'description': 'Machine learning and data tooling', 'sort_order': 3},
    {'id': 'cat-programming', 'name': 'Programming', 'description': 'General languages and fundamentals', 'sort_order': 4},
    {'id': 'cat-languages', 'name': 'Languages', 'description': 'Spoken languages', 'sort_order': 5},
]

SKILLS = [
    {'id': 'skill-angular', 'category_id': 'cat-frontend', 'name': 'Angular', 'years_of_experience': 2, 'icon_key': 'angular', 'sort_order': 1, 'is_highlighted': True, 'created_at': TIMESTAMP},
    {'id': 'skill-tailwind', 'category_id': 'cat-frontend', 'name': 'Tailwind CSS', 'years_of_experience': 1, 'icon_key': 'tailwind', 'sort_order': 2, 'is_highlighted': True, 'created_at': TIMESTAMP},
    {'id': 'skill-typescript', 'category_id': 'cat-frontend', 'name': 'TypeScript', 'years_of_experience': 2, 'icon_key': 'typescript', 'sort_order': 3, 'is_highlighted': True, 'created_at': TIMESTAMP},
    {'id': 'skill-react', 'category_id': 'cat-frontend', 'name': 'React', 'years_of_experience': 1, 'icon_key': 'react', 'sort_order': 4, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-ux', 'category_id': 'cat-frontend', 'name': 'UX', 'years_of_experience': 1, 'icon_key': 'layout', 'sort_order': 5, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-state-management', 'category_id': 'cat-frontend', 'name': 'State Management', 'years_of_experience': 1, 'icon_key': 'state', 'sort_order': 6, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-nx', 'category_id': 'cat-frontend', 'name': 'Nx', 'years_of_experience': 1, 'icon_key': 'nx', 'sort_order': 7, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-laravel', 'category_id': 'cat-backend', 'name': 'Laravel', 'years_of_experience': 2, 'icon_key': 'laravel', 'sort_order': 1, 'is_highlighted': True, 'created_at': TIMESTAMP},
    {'id': 'skill-dotnet', 'category_id': 'cat-backend', 'name': '.NET', 'years_of_experience': 1, 'icon_key': 'dotnet', 'sort_order': 2, 'is_highlighted': True, 'created_at': TIMESTAMP},
    {'id': 'skill-rest', 'category_id': 'cat-backend', 'name': 'REST APIs', 'years_of_experience': 2, 'icon_key': 'api', 'sort_order': 3, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-livewire', 'category_id': 'cat-backend', 'name': 'Livewire', 'years_of_experience': 1, 'icon_key': 'livewire', 'sort_order': 4, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-spring-boot', 'category_id': 'cat-backend', 'name': 'Spring Boot', 'years_of_experience': 1, 'icon_key': 'spring', 'sort_order': 5, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-python', 'category_id': 'cat-ai', 'name': 'Python', 'years_of_experience': 2, 'icon_key': 'python', 'sort_order': 1, 'is_highlighted': True, 'created_at': TIMESTAMP},
    {'id': 'skill-tensorflow', 'category_id': 'cat-ai', 'name': 'TensorFlow', 'years_of_experience': 1, 'icon_key': 'tensorflow', 'sort_order': 2, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-data-prep', 'category_id': 'cat-ai', 'name': 'Data Prep', 'years_of_experience': 1, 'icon_key': 'dataset', 'sort_order': 3, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-efficientnet', 'category_id': 'cat-ai', 'name': 'EfficientNet', 'years_of_experience': 1, 'icon_key': 'model', 'sort_order': 4, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-ml', 'category_id': 'cat-ai', 'name': 'ML', 'years_of_experience': 1, 'icon_key': 'ml', 'sort_order': 5, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-java', 'category_id': 'cat-programming', 'name': 'Java', 'years_of_experience': 2, 'icon_key': 'java', 'sort_order': 1, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-csharp', 'category_id': 'cat-programming', 'name': 'C#', 'years_of_experience': 1, 'icon_key': 'csharp', 'sort_order': 2, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-design-patterns', 'category_id': 'cat-programming', 'name': 'Design Patterns', 'years_of_experience': 1, 'icon_key': 'patterns', 'sort_order': 4, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-dutch', 'category_id': 'cat-languages', 'name': 'Dutch', 'years_of_experience': None, 'icon_key': None, 'sort_order': 1, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-english', 'category_id': 'cat-languages', 'name': 'English', 'years_of_experience': None, 'icon_key': None, 'sort_order': 2, 'is_highlighted': False, 'created_at': TIMESTAMP},
    {'id': 'skill-french', 'category_id': 'cat-languages', 'name': 'French', 'years_of_experience': None, 'icon_key': None, 'sort_order': 3, 'is_highlighted': False, 'created_at': TIMESTAMP},
]

EXPERIENCES = [
    {
        'id': 'experience-internship-client-work',
        'organization_name': 'Client delivery team',
        'role_title': 'Internship',
        'location': 'Geel, Belgium',
        'experience_type': 'internship',
        'start_date': date(2025, 2, 1),
        'end_date': date(2025, 6, 30),
        'is_current': False,
        'summary': 'Worked on maintainable web interfaces, internal tooling, and clear communication with clients while shipping practical features in a team setting.',
        'description_markdown': 'Collaborated in a client-facing team on practical web features, internal tools, and documentation.',
        'sort_order': 1,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'experience-thomas-more',
        'organization_name': 'Thomas More',
        'role_title': 'Applied Computer Science',
        'location': 'Geel, Belgium',
        'experience_type': 'education',
        'start_date': date(2022, 9, 1),
        'end_date': None,
        'is_current': True,
        'summary': 'Built projects across AI, software engineering, and web development, with a strong focus on hands-on delivery and iterative improvement.',
        'description_markdown': 'Worked on AI, web, and software engineering assignments with practical delivery and reflection.',
        'sort_order': 2,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
    {
        'id': 'experience-personal-projects',
        'organization_name': 'Independent work',
        'role_title': 'Personal Projects',
        'location': 'Remote',
        'experience_type': 'personal',
        'start_date': date(2023, 1, 1),
        'end_date': None,
        'is_current': True,
        'summary': 'Created portfolio, API, machine learning, and full-stack projects to sharpen real-world architecture, deployment, and UI skills.',
        'description_markdown': 'Used personal projects to practice architecture, deployment, and maintainable front-end work.',
        'sort_order': 3,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    },
]

EXPERIENCE_SKILLS = [
    ('experience-internship-client-work', 'skill-angular'),
    ('experience-internship-client-work', 'skill-rest'),
    ('experience-internship-client-work', 'skill-typescript'),
    ('experience-thomas-more', 'skill-python'),
    ('experience-thomas-more', 'skill-laravel'),
    ('experience-thomas-more', 'skill-dotnet'),
    ('experience-personal-projects', 'skill-angular'),
    ('experience-personal-projects', 'skill-tailwind'),
    ('experience-personal-projects', 'skill-design-patterns'),
]

GITHUB_SNAPSHOT = {
    'id': 'github-snapshot-2025-10-01',
    'snapshot_date': date(2025, 10, 1),
    'username': 'shuzu',
    'public_repo_count': 24,
    'followers_count': 18,
    'following_count': 25,
    'total_stars': 37,
    'total_commits': 512,
    'raw_payload': {'source': 'seed'},
    'created_at': datetime(2025, 10, 1, 8, 0, tzinfo=UTC),
}

CONTRIBUTION_LEVELS = [
    1, 2, 2, 1, 3, 2, 1, 2, 3, 2, 1, 1, 2, 3,
    1, 1, 2, 3, 2, 1, 1, 2, 2, 3, 1, 4, 2, 1,
]


def _seed_uuid(value: str | None) -> UUID | None:
    if value is None:
        return None
    return seed_uuid(value)


def _with_uuid_fields(payload: dict, *field_names: str) -> dict:
    data = dict(payload)
    for field_name in field_names:
        if field_name in data:
            data[field_name] = _seed_uuid(data[field_name])
    return data


def _parse_date(value: str | None) -> date | None:
    if value is None:
        return None
    return date.fromisoformat(value)


def _parse_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    if value.endswith('Z'):
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, '%B %d, %Y').replace(tzinfo=UTC)


def seed_database(session: Session) -> None:
    already_seeded = session.scalar(select(Project.id).limit(1))
    if already_seeded:
        return

    try:
        session.add_all([NavigationItem(**_with_uuid_fields(item, 'id')) for item in NAVIGATION_ITEMS])
        session.add_all([MediaFile(**_with_uuid_fields(item, 'id', 'uploaded_by_id')) for item in MEDIA_FILES])
        session.add_all([SkillCategory(**_with_uuid_fields(item, 'id')) for item in SKILL_CATEGORIES])
        session.add_all([Skill(**_with_uuid_fields(item, 'id', 'category_id')) for item in SKILLS])
        session.add(GithubSnapshot(**_with_uuid_fields(GITHUB_SNAPSHOT, 'id')))
        session.add(
            Profile(
                id=_seed_uuid(PROFILE_ROW['id']),
                first_name=PROFILE_ROW['first_name'],
                last_name=PROFILE_ROW['last_name'],
                headline=PROFILE_ROW['headline'],
                short_intro=PROFILE_ROW['short_intro'],
                long_bio=PROFILE_ROW['long_bio'],
                location=PROFILE_ROW['location'],
                email=PROFILE_ROW['email'],
                phone=PROFILE_ROW['phone'],
                avatar_file_id=_seed_uuid(PROFILE_ROW['avatar_file_id']),
                hero_image_file_id=_seed_uuid(PROFILE_ROW['hero_image_file_id']),
                resume_file_id=_seed_uuid(PROFILE_ROW['resume_file_id']),
                cta_primary_label=PROFILE_ROW['cta_primary_label'],
                cta_primary_url=PROFILE_ROW['cta_primary_url'],
                cta_secondary_label=PROFILE_ROW['cta_secondary_label'],
                cta_secondary_url=PROFILE_ROW['cta_secondary_url'],
                is_public=PROFILE_ROW['is_public'],
                created_at=_parse_datetime(PROFILE_ROW['created_at']) or TIMESTAMP,
                updated_at=_parse_datetime(PROFILE_ROW['updated_at']) or TIMESTAMP,
            )
        )
        session.flush()

        session.add_all([SocialLink(**_with_uuid_fields(item, 'id', 'profile_id')) for item in SOCIAL_LINKS])
        session.add_all([Experience(**_with_uuid_fields(item, 'id', 'logo_file_id')) for item in EXPERIENCES])
        session.add_all(
            [
                GithubContributionDay(
                    id=seed_uuid(f'github-day-{index + 1}'),
                    snapshot_id=_seed_uuid(GITHUB_SNAPSHOT['id']),
                    contribution_date=date(2025, 1, (index % 28) + 1),
                    contribution_count=level * 3,
                    level=level,
                )
                for index, level in enumerate(CONTRIBUTION_LEVELS)
            ]
        )
        session.flush()

        session.add_all(
            [ExperienceSkill(experience_id=seed_uuid(experience_id), skill_id=seed_uuid(skill_id)) for experience_id, skill_id in EXPERIENCE_SKILLS]
        )
        session.flush()

        skill_name_to_id = {skill['name']: seed_uuid(skill['id']) for skill in SKILLS}
        for project in PROJECT_ROWS:
            github_owner = None
            if project.get('github_url') and 'github.com/' in project['github_url']:
                github_owner = project['github_url'].rstrip('/').split('/')[-1]
            github_repo_name = project.get('github_repo_name')

            session.add(
                Project(
                    id=_seed_uuid(project['id']),
                    slug=project['slug'],
                    title=project['title'],
                    teaser=project['teaser'],
                    summary=project['summary'],
                    description_markdown=project['description_markdown'],
                    cover_image_file_id=_seed_uuid(project['cover_image_file_id']),
                    github_url=project.get('github_url'),
                    github_repo_owner=github_owner,
                    github_repo_name=github_repo_name,
                    demo_url=project.get('demo_url'),
                    company_name=project.get('company_name'),
                    started_on=_parse_date(project.get('started_on')),
                    ended_on=_parse_date(project.get('ended_on')),
                    duration_label=project['duration_label'],
                    status=project['status'],
                    state=ProjectState(project['state']),
                    is_featured=project['is_featured'],
                    sort_order=project['sort_order'],
                    published_at=_parse_datetime(project['published_at']) or TIMESTAMP,
                    created_at=_parse_datetime(project.get('created_at')) or TIMESTAMP,
                    updated_at=_parse_datetime(project.get('updated_at')) or TIMESTAMP,
                )
            )
        session.flush()

        for project in PROJECT_ROWS:
            session.add(
                ProjectImage(
                    project_id=_seed_uuid(project['id']),
                    image_file_id=_seed_uuid(project['cover_image_file_id']),
                    alt_text=project.get('cover_image_alt'),
                    sort_order=0,
                    is_cover=True,
                )
            )
            for skill_name in PROJECT_SKILL_NAMES_BY_PROJECT_SLUG.get(project['slug'], []):
                skill_id = skill_name_to_id.get(skill_name)
                if skill_id:
                    session.add(ProjectSkill(project_id=_seed_uuid(project['id']), skill_id=skill_id))
        session.flush()

        seen_tags: dict[str, str] = {}
        for post in BLOG_POST_ROWS:
            for tag_name in BLOG_TAG_NAMES_BY_POST_SLUG.get(post['slug'], []):
                tag_slug = tag_name.lower().replace(' ', '-').replace('&', 'and')
                if tag_slug not in seen_tags:
                    tag_id = seed_uuid(f'tag-{tag_slug}')
                    seen_tags[tag_slug] = tag_id
                    session.add(BlogTag(id=tag_id, name=tag_name, slug=tag_slug))
        session.flush()

        for post in BLOG_POST_ROWS:
            session.add(
                BlogPost(
                    id=_seed_uuid(post.get('id')),
                    slug=post['slug'],
                    title=post['title'],
                    excerpt=post['excerpt'],
                    content_markdown=post['content_markdown'],
                    cover_image_file_id=_seed_uuid(post.get('cover_image_file_id')), 
                    cover_image_alt=post.get('cover_image_alt'),
                    reading_time_minutes=post.get('reading_time_minutes'),
                    status=PublicationStatus(post['status']),
                    is_featured=post['is_featured'],
                    published_at=_parse_datetime(post['published_at']) or TIMESTAMP,
                    seo_title=post.get('seo_title'),
                    seo_description=post.get('seo_description'),
                    created_at=_parse_datetime(post.get('created_at')) or TIMESTAMP,
                    updated_at=_parse_datetime(post.get('updated_at')) or TIMESTAMP,
                )
            )
        session.flush()

        for post in BLOG_POST_ROWS:
            for tag_name in BLOG_TAG_NAMES_BY_POST_SLUG.get(post['slug'], []):
                tag_slug = tag_name.lower().replace(' ', '-').replace('&', 'and')
                session.add(BlogPostTag(post_id=_seed_uuid(post.get('id')), tag_id=seen_tags[tag_slug]))

        session.commit()
    except Exception:
        session.rollback()
        raise
