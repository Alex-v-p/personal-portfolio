from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
import os
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from infra.postgres.bootstrap.seed_content import (
    BLOG_POST_ROWS,
    BLOG_TAG_NAMES_BY_POST_SLUG,
    PROFILE_ROW,
    PROJECT_ROWS,
    PROJECT_SKILL_NAMES_BY_PROJECT_SLUG,
)
from infra.postgres.bootstrap.seed_ids import seed_uuid
from app.db.models import (
    AdminUser,
    BlogPost,
    BlogPostTag,
    BlogTag,
    EventType,
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
    SiteEvent,
    Skill,
    SkillCategory,
    SocialLink,
)

NAVIGATION_ITEMS = [{'id': 'nav-home', 'label': 'Home', 'route_path': '/', 'is_external': False, 'sort_order': 1, 'is_visible': True},
 {'id': 'nav-projects',
  'label': 'Projects',
  'route_path': '/projects',
  'is_external': False,
  'sort_order': 2,
  'is_visible': True},
 {'id': 'nav-blog', 'label': 'Blog', 'route_path': '/blog', 'is_external': False, 'sort_order': 3, 'is_visible': True},
 {'id': 'nav-contact',
  'label': 'Contact',
  'route_path': '/contact',
  'is_external': False,
  'sort_order': 4,
  'is_visible': True},
 {'id': 'nav-stats',
  'label': 'Stats',
  'route_path': '/stats',
  'is_external': False,
  'sort_order': 5,
  'is_visible': True},
 {'id': 'nav-assistant',
  'label': 'Assistant',
  'route_path': '/assistant',
  'is_external': False,
  'sort_order': 6,
  'is_visible': False}]

TIMESTAMP = datetime(2026, 4, 1, 9, 0, tzinfo=UTC)

_pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')


def _admin_user_seed() -> dict:
    return {
        'id': 'admin-primary',
        'email': os.getenv('ADMIN_EMAIL', 'admin@example.com').strip().lower(),
        'password': os.getenv('ADMIN_PASSWORD', 'change-me-admin'),
        'display_name': os.getenv('ADMIN_DISPLAY_NAME', 'Portfolio Admin').strip() or 'Portfolio Admin',
        'is_active': True,
        'created_at': TIMESTAMP,
        'updated_at': TIMESTAMP,
    }


MEDIA_FILES = [{'id': 'file-avatar-alex',
  'bucket_name': 'portfolio',
  'object_key': 'profiles/alex/avatar.png',
  'original_filename': 'alex-avatar.png',
  'stored_filename': 'alex-avatar.png',
  'mime_type': 'image/png',
  'file_size_bytes': 248130,
  'checksum': 'sha256-avatar-alex',
  'public_url': None,
  'alt_text': 'Portrait placeholder for Alex van Poppel',
  'title': 'Profile avatar',
  'description': 'Placeholder profile portrait generated for local seed data.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-hero-portrait',
  'bucket_name': 'portfolio',
  'object_key': 'profiles/alex/hero.png',
  'original_filename': 'hero.png',
  'stored_filename': 'hero.png',
  'mime_type': 'image/png',
  'file_size_bytes': 612004,
  'checksum': 'sha256-hero-alex',
  'public_url': None,
  'alt_text': 'Hero portrait placeholder for Alex van Poppel',
  'title': 'Hero portrait',
  'description': 'Placeholder hero portrait generated for local seed data.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-resume',
  'bucket_name': 'portfolio',
  'object_key': 'profiles/alex/resume.pdf',
  'original_filename': 'alex-van-poppel-resume.pdf',
  'stored_filename': 'alex-van-poppel-resume.pdf',
  'mime_type': 'application/pdf',
  'file_size_bytes': 152320,
  'checksum': 'sha256-resume-alex',
  'public_url': None,
  'alt_text': 'Resume PDF for Alex van Poppel',
  'title': 'Resume',
  'description': 'Simple placeholder resume generated for local seed data.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-project-portfolio-rebuild-cover',
  'bucket_name': 'portfolio',
  'object_key': 'projects/portfolio-rebuild/cover.png',
  'original_filename': 'portfolio-rebuild-cover.png',
  'stored_filename': 'portfolio-rebuild-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 480221,
  'checksum': 'sha256-project-portfolio-rebuild-cover',
  'public_url': None,
  'alt_text': 'Portfolio rebuild cover with CMS and API themes',
  'title': 'Portfolio rebuild cover',
  'description': 'Placeholder cover for the portfolio rebuild project.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-project-laravel-portfolio-cover',
  'bucket_name': 'portfolio',
  'object_key': 'projects/laravel-portfolio/cover.png',
  'original_filename': 'laravel-portfolio-cover.png',
  'stored_filename': 'laravel-portfolio-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 390110,
  'checksum': 'sha256-project-laravel-portfolio-cover',
  'public_url': None,
  'alt_text': 'Laravel portfolio cover with cards and self-hosting theme',
  'title': 'Laravel portfolio cover',
  'description': 'Placeholder cover for the Laravel portfolio project.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-project-placement-cover',
  'bucket_name': 'portfolio',
  'object_key': 'projects/placement-prediction/cover.png',
  'original_filename': 'placement-prediction-cover.png',
  'stored_filename': 'placement-prediction-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 400235,
  'checksum': 'sha256-project-placement-cover',
  'public_url': None,
  'alt_text': 'Machine learning project cover with charts and model cards',
  'title': 'Placement prediction cover',
  'description': 'Placeholder cover for the placement prediction project.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-project-iot-cover',
  'bucket_name': 'portfolio',
  'object_key': 'projects/iot-security-system/cover.png',
  'original_filename': 'iot-security-cover.png',
  'stored_filename': 'iot-security-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 360421,
  'checksum': 'sha256-project-iot-cover',
  'public_url': None,
  'alt_text': 'IoT turret project cover with hardware and computer vision theme',
  'title': 'IoT security cover',
  'description': 'Placeholder cover for the IoT security project.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-project-analysis-cover',
  'bucket_name': 'portfolio',
  'object_key': 'projects/training-session-analysis/cover.png',
  'original_filename': 'training-session-analysis-cover.png',
  'stored_filename': 'training-session-analysis-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 342111,
  'checksum': 'sha256-project-analysis-cover',
  'public_url': None,
  'alt_text': 'Analysis project cover with workshops, diagrams, and prototype notes',
  'title': 'Training analysis cover',
  'description': 'Placeholder cover for the analysis project.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-project-exchange-cover',
  'bucket_name': 'portfolio',
  'object_key': 'projects/exchange-student-portal/cover.png',
  'original_filename': 'exchange-student-portal-cover.png',
  'stored_filename': 'exchange-student-portal-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 320811,
  'checksum': 'sha256-project-exchange-cover',
  'public_url': None,
  'alt_text': 'Exchange portal cover with travel, planning, and student workflow theme',
  'title': 'Exchange portal cover',
  'description': 'Placeholder cover for the exchange portal project.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-blog-portfolio-rebuild-cover',
  'bucket_name': 'portfolio',
  'object_key': 'blog/rebuilding-my-portfolio/cover.png',
  'original_filename': 'blog-portfolio-rebuild-cover.png',
  'stored_filename': 'blog-portfolio-rebuild-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 312213,
  'checksum': 'sha256-blog-portfolio-rebuild-cover',
  'public_url': None,
  'alt_text': 'Blog cover for rebuilding a portfolio platform',
  'title': 'Portfolio rebuild blog cover',
  'description': 'Placeholder cover for the portfolio rebuild article.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-blog-iot-cover',
  'bucket_name': 'portfolio',
  'object_key': 'blog/iot-security-turret-lessons/cover.png',
  'original_filename': 'blog-iot-cover.png',
  'stored_filename': 'blog-iot-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 315773,
  'checksum': 'sha256-blog-iot-cover',
  'public_url': None,
  'alt_text': 'Blog cover about lessons from an IoT security project',
  'title': 'IoT lessons blog cover',
  'description': 'Placeholder cover for the IoT article.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-blog-analysis-cover',
  'bucket_name': 'portfolio',
  'object_key': 'blog/client-workshops-analysis/cover.png',
  'original_filename': 'blog-analysis-cover.png',
  'stored_filename': 'blog-analysis-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 302921,
  'checksum': 'sha256-blog-analysis-cover',
  'public_url': None,
  'alt_text': 'Blog cover about client workshops and requirements analysis',
  'title': 'Analysis blog cover',
  'description': 'Placeholder cover for the analysis article.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'file-blog-placement-cover',
  'bucket_name': 'portfolio',
  'object_key': 'blog/placement-model-notes/cover.png',
  'original_filename': 'blog-placement-cover.png',
  'stored_filename': 'blog-placement-cover.png',
  'mime_type': 'image/png',
  'file_size_bytes': 302921,
  'checksum': 'sha256-blog-placement-cover',
  'public_url': None,
  'alt_text': 'Blog cover about cleaning data for a machine learning model',
  'title': 'Placement model blog cover',
  'description': 'Placeholder cover for the placement model article.',
  'visibility': 'public',
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'}]

SOCIAL_LINKS = [{'id': 'social-github',
  'profile_id': 'profile-alex-van-poppel',
  'platform': 'github',
  'label': 'GitHub',
  'url': 'https://github.com/shuzu',
  'icon_key': 'github',
  'sort_order': 1,
  'is_visible': True},
 {'id': 'social-linkedin',
  'profile_id': 'profile-alex-van-poppel',
  'platform': 'linkedin',
  'label': 'LinkedIn',
  'url': 'https://www.linkedin.com/in/alex-v-p/',
  'icon_key': 'linkedin',
  'sort_order': 2,
  'is_visible': True},
 {'id': 'social-email',
  'profile_id': 'profile-alex-van-poppel',
  'platform': 'email',
  'label': 'Email',
  'url': 'mailto:alex@shuzu.dev',
  'icon_key': 'mail',
  'sort_order': 3,
  'is_visible': True}]

SKILL_CATEGORIES = [{'id': 'cat-frontend', 'name': 'Front-End', 'description': 'UI and browser-facing development', 'sort_order': 1},
 {'id': 'cat-backend', 'name': 'Back-End', 'description': 'Server-side development and APIs', 'sort_order': 2},
 {'id': 'cat-data', 'name': 'Data & AI', 'description': 'Data preparation, analysis, and ML tooling', 'sort_order': 3},
 {'id': 'cat-tools',
  'name': 'Infrastructure & Tools',
  'description': 'Deployment, systems, and technical tooling',
  'sort_order': 4},
 {'id': 'cat-analysis',
  'name': 'Analysis & Collaboration',
  'description': 'Workshops, modelling, and communication',
  'sort_order': 5},
 {'id': 'cat-languages', 'name': 'Languages', 'description': 'Spoken languages', 'sort_order': 6}]

SKILLS = [{'id': 'skill-html',
  'category_id': 'cat-frontend',
  'name': 'HTML',
  'years_of_experience': 3,
  'icon_key': 'html',
  'sort_order': 1,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-css',
  'category_id': 'cat-frontend',
  'name': 'CSS',
  'years_of_experience': 3,
  'icon_key': 'css',
  'sort_order': 2,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-tailwind',
  'category_id': 'cat-frontend',
  'name': 'Tailwind CSS',
  'years_of_experience': 2,
  'icon_key': 'tailwind',
  'sort_order': 3,
  'is_highlighted': True,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-alpine',
  'category_id': 'cat-frontend',
  'name': 'Alpine.js',
  'years_of_experience': 1,
  'icon_key': 'alpine',
  'sort_order': 4,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-livewire',
  'category_id': 'cat-frontend',
  'name': 'Livewire',
  'years_of_experience': 2,
  'icon_key': 'livewire',
  'sort_order': 5,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-angular',
  'category_id': 'cat-frontend',
  'name': 'Angular',
  'years_of_experience': 1,
  'icon_key': 'angular',
  'sort_order': 6,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-react',
  'category_id': 'cat-frontend',
  'name': 'React',
  'years_of_experience': 1,
  'icon_key': 'react',
  'sort_order': 7,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-typescript',
  'category_id': 'cat-frontend',
  'name': 'TypeScript',
  'years_of_experience': 1,
  'icon_key': 'typescript',
  'sort_order': 8,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-laravel',
  'category_id': 'cat-backend',
  'name': 'Laravel',
  'years_of_experience': 2,
  'icon_key': 'laravel',
  'sort_order': 1,
  'is_highlighted': True,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-fastapi',
  'category_id': 'cat-backend',
  'name': 'FastAPI',
  'years_of_experience': 1,
  'icon_key': 'fastapi',
  'sort_order': 2,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-rest',
  'category_id': 'cat-backend',
  'name': 'REST APIs',
  'years_of_experience': 2,
  'icon_key': 'api',
  'sort_order': 3,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-java',
  'category_id': 'cat-backend',
  'name': 'Java',
  'years_of_experience': 2,
  'icon_key': 'java',
  'sort_order': 4,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-csharp',
  'category_id': 'cat-backend',
  'name': 'C#',
  'years_of_experience': 1,
  'icon_key': 'csharp',
  'sort_order': 5,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-sql',
  'category_id': 'cat-backend',
  'name': 'SQL',
  'years_of_experience': 2,
  'icon_key': 'database',
  'sort_order': 6,
  'is_highlighted': True,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-sqlite',
  'category_id': 'cat-backend',
  'name': 'SQLite',
  'years_of_experience': 2,
  'icon_key': 'sqlite',
  'sort_order': 7,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-python',
  'category_id': 'cat-data',
  'name': 'Python',
  'years_of_experience': 3,
  'icon_key': 'python',
  'sort_order': 1,
  'is_highlighted': True,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-pandas',
  'category_id': 'cat-data',
  'name': 'Pandas',
  'years_of_experience': 1,
  'icon_key': 'pandas',
  'sort_order': 2,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-matplotlib',
  'category_id': 'cat-data',
  'name': 'Matplotlib',
  'years_of_experience': 1,
  'icon_key': 'chart',
  'sort_order': 3,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-sklearn',
  'category_id': 'cat-data',
  'name': 'Scikit-learn',
  'years_of_experience': 1,
  'icon_key': 'ml',
  'sort_order': 4,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-ml',
  'category_id': 'cat-data',
  'name': 'Machine Learning',
  'years_of_experience': 1,
  'icon_key': 'brain',
  'sort_order': 5,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-git',
  'category_id': 'cat-tools',
  'name': 'Git',
  'years_of_experience': 3,
  'icon_key': 'git',
  'sort_order': 1,
  'is_highlighted': True,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-docker',
  'category_id': 'cat-tools',
  'name': 'Docker',
  'years_of_experience': 1,
  'icon_key': 'docker',
  'sort_order': 2,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-linux',
  'category_id': 'cat-tools',
  'name': 'Linux',
  'years_of_experience': 2,
  'icon_key': 'linux',
  'sort_order': 3,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-networking',
  'category_id': 'cat-tools',
  'name': 'Networking',
  'years_of_experience': 2,
  'icon_key': 'network',
  'sort_order': 4,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-orange-pi',
  'category_id': 'cat-tools',
  'name': 'Orange Pi',
  'years_of_experience': 1,
  'icon_key': 'chip',
  'sort_order': 5,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-freecad',
  'category_id': 'cat-tools',
  'name': 'FreeCAD',
  'years_of_experience': 1,
  'icon_key': 'cube',
  'sort_order': 6,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-nx',
  'category_id': 'cat-tools',
  'name': 'Nx',
  'years_of_experience': 1,
  'icon_key': 'nx',
  'sort_order': 7,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-self-hosting',
  'category_id': 'cat-tools',
  'name': 'Self-hosting',
  'years_of_experience': 2,
  'icon_key': 'server',
  'sort_order': 8,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-iot-electronics',
  'category_id': 'cat-tools',
  'name': 'IoT Electronics',
  'years_of_experience': 1,
  'icon_key': 'cpu',
  'sort_order': 9,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-req-analysis',
  'category_id': 'cat-analysis',
  'name': 'Requirements Analysis',
  'years_of_experience': 2,
  'icon_key': 'clipboard',
  'sort_order': 1,
  'is_highlighted': True,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-prototyping',
  'category_id': 'cat-analysis',
  'name': 'Prototyping',
  'years_of_experience': 2,
  'icon_key': 'layout',
  'sort_order': 2,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-uml',
  'category_id': 'cat-analysis',
  'name': 'UML',
  'years_of_experience': 1,
  'icon_key': 'diagram',
  'sort_order': 3,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-formal-communication',
  'category_id': 'cat-analysis',
  'name': 'Formal Communication',
  'years_of_experience': 2,
  'icon_key': 'message-square',
  'sort_order': 4,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-team-workshops',
  'category_id': 'cat-analysis',
  'name': 'Team Workshops',
  'years_of_experience': 2,
  'icon_key': 'users',
  'sort_order': 5,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-dutch',
  'category_id': 'cat-languages',
  'name': 'Dutch',
  'years_of_experience': None,
  'icon_key': None,
  'sort_order': 1,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-english',
  'category_id': 'cat-languages',
  'name': 'English',
  'years_of_experience': None,
  'icon_key': None,
  'sort_order': 2,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'},
 {'id': 'skill-portuguese',
  'category_id': 'cat-languages',
  'name': 'Portuguese',
  'years_of_experience': None,
  'icon_key': None,
  'sort_order': 3,
  'is_highlighted': False,
  'created_at': 'TIMESTAMP'}]

EXPERIENCES = [{'id': 'experience-thomas-more',
  'organization_name': 'Thomas More University of Applied Sciences',
  'role_title': 'Applied Computer Science',
  'location': 'Geel, Belgium',
  'experience_type': 'education',
  'start_date': '2023-09-01',
  'end_date': None,
  'is_current': True,
  'summary': 'Building projects across web development, software engineering, AI, and analysis while growing a '
             'stronger interest in maintainable architecture and practical delivery.',
  'description_markdown': 'Coursework and projects in web, software, data, and communication, with a strong focus on '
                          'turning assignments into portfolio-ready work.',
  'logo_file_id': None,
  'sort_order': 1,
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'experience-provil',
  'organization_name': 'Provil Institute Lommel',
  'role_title': 'Programming & Web Foundations',
  'location': 'Lommel, Belgium',
  'experience_type': 'education',
  'start_date': '2022-09-01',
  'end_date': '2023-06-30',
  'is_current': False,
  'summary': 'Built a foundation in programming, web development, and problem solving before moving into higher '
             'education.',
  'description_markdown': 'Focused on the fundamentals that later made larger software and web projects easier to '
                          'approach.',
  'logo_file_id': None,
  'sort_order': 2,
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'experience-self-hosting',
  'organization_name': 'Independent work',
  'role_title': 'Self-hosting & Homelab Projects',
  'location': 'Remote',
  'experience_type': 'personal',
  'start_date': '2024-01-01',
  'end_date': None,
  'is_current': True,
  'summary': 'Used personal infrastructure projects to learn more about servers, routing, storage, networking, and '
             'what deployment changes about a software build.',
  'description_markdown': 'Explored self-hosting, reverse proxies, NAS tooling, virtual machines, and other practical '
                          'infrastructure concerns around personal software projects.',
  'logo_file_id': None,
  'sort_order': 3,
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'},
 {'id': 'experience-client-analysis',
  'organization_name': 'Team-based coursework',
  'role_title': 'Client workshops & analysis projects',
  'location': 'Geel, Belgium',
  'experience_type': 'project',
  'start_date': '2024-10-01',
  'end_date': '2025-06-30',
  'is_current': False,
  'summary': 'Worked in teams on workshop-style projects where stakeholder questions, documentation, prioritisation, '
             'and prototypes mattered just as much as the technical solution.',
  'description_markdown': 'Included client communication, requirements analysis, presentation work, and collaborative '
                          'planning for school projects.',
  'logo_file_id': None,
  'sort_order': 4,
  'created_at': 'TIMESTAMP',
  'updated_at': 'TIMESTAMP'}]

EXPERIENCE_SKILLS = [('experience-thomas-more', 'skill-python'),
 ('experience-thomas-more', 'skill-laravel'),
 ('experience-thomas-more', 'skill-sql'),
 ('experience-thomas-more', 'skill-req-analysis'),
 ('experience-provil', 'skill-html'),
 ('experience-provil', 'skill-css'),
 ('experience-provil', 'skill-python'),
 ('experience-self-hosting', 'skill-docker'),
 ('experience-self-hosting', 'skill-linux'),
 ('experience-self-hosting', 'skill-networking'),
 ('experience-self-hosting', 'skill-self-hosting'),
 ('experience-client-analysis', 'skill-req-analysis'),
 ('experience-client-analysis', 'skill-prototyping'),
 ('experience-client-analysis', 'skill-formal-communication'),
 ('experience-client-analysis', 'skill-team-workshops')]


def _build_seed_github_contributions() -> tuple[list[dict], int]:
    snapshot_date = date(2026, 4, 1)
    start_date = snapshot_date - timedelta(days=364)
    rows: list[dict] = []
    total_commits = 0

    for index in range(365):
        contribution_date = start_date + timedelta(days=index)
        if contribution_date.weekday() >= 5:
            level = 0 if index % 5 == 0 else (1 if index % 2 == 0 else 2)
        else:
            cycle = (index * 7 + contribution_date.month * 3 + contribution_date.day) % 9
            if cycle in (0, 1):
                level = 1
            elif cycle in (2, 3, 4):
                level = 2
            elif cycle in (5, 6):
                level = 3
            elif cycle == 7:
                level = 4
            else:
                level = 0

        if contribution_date.month in (1, 2, 3) and contribution_date.weekday() < 5 and index % 11 == 0:
            level = min(4, level + 1)

        count = [0, 2, 5, 9, 14][level]
        total_commits += count
        rows.append({
            'id': f'github-day-{index + 1}',
            'snapshot_id': 'github-snapshot-2026-04-01',
            'contribution_date': contribution_date,
            'contribution_count': count,
            'level': level,
        })

    return rows, total_commits


CONTRIBUTION_DAYS, TOTAL_SEEDED_COMMITS = _build_seed_github_contributions()

GITHUB_SNAPSHOT = {
    'id': 'github-snapshot-2026-04-01',
    'snapshot_date': date(2026, 4, 1),
    'username': 'shuzu',
    'public_repo_count': 26,
    'followers_count': 21,
    'following_count': 29,
    'total_stars': 48,
    'total_commits': TOTAL_SEEDED_COMMITS,
    'raw_payload': {'source': 'seed'},
    'created_at': datetime(2026, 4, 1, 8, 0, tzinfo=UTC),
}


def _build_site_event_rows() -> list[dict]:
    rows: list[dict] = []
    page_paths = ['/', '/projects', '/blog', '/stats', '/contact']
    base_time = datetime(2026, 4, 1, 18, 0, tzinfo=UTC)

    def add_rows(prefix: str, count: int, event_type: EventType, page_choices: list[str]) -> None:
        for index in range(count):
            created_at = base_time - timedelta(days=(index * 3) % 120, hours=index % 6, minutes=(index * 11) % 60)
            rows.append({
                'id': f'{prefix}-{index + 1}',
                'session_id': f'seed-session-{(index % 44) + 1}',
                'visitor_id': f'seed-visitor-{(index % 91) + 1}',
                'page_path': page_choices[index % len(page_choices)],
                'event_type': event_type,
                'referrer': 'https://www.google.com' if index % 3 else 'https://github.com',
                'user_agent': 'seed-browser/1.0',
                'metadata_json': {'seeded': True},
                'created_at': created_at,
            })

    add_rows('event-page-view', 286, EventType.PAGE_VIEW, page_paths)
    add_rows('event-like', 37, EventType.PORTFOLIO_LIKE, ['/'])
    add_rows('event-blog-view', 91, EventType.BLOG_VIEW, ['/blog'])
    add_rows('event-project-click', 73, EventType.PROJECT_CLICK, ['/projects'])
    return rows


SITE_EVENT_ROWS = _build_site_event_rows()


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
    if value == 'TIMESTAMP':
        return TIMESTAMP
    if value.endswith('Z'):
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, '%B %d, %Y').replace(tzinfo=UTC)


def _upsert_admin_user(session: Session) -> None:
    admin_user_seed = _admin_user_seed()
    admin_user_id = _seed_uuid(admin_user_seed['id'])

    existing_admin = session.scalar(select(AdminUser).where(AdminUser.id == admin_user_id))
    if existing_admin is None:
        existing_admin = session.scalar(select(AdminUser).where(AdminUser.email == admin_user_seed['email']))

    if existing_admin is None:
        session.add(
            AdminUser(
                id=admin_user_id,
                email=admin_user_seed['email'],
                password_hash=_pwd_context.hash(admin_user_seed['password']),
                display_name=admin_user_seed['display_name'],
                is_active=admin_user_seed['is_active'],
                created_at=admin_user_seed['created_at'],
                updated_at=admin_user_seed['updated_at'],
            )
        )
        session.flush()
        return

    existing_admin.email = admin_user_seed['email']
    existing_admin.password_hash = _pwd_context.hash(admin_user_seed['password'])
    existing_admin.display_name = admin_user_seed['display_name']
    existing_admin.is_active = admin_user_seed['is_active']
    existing_admin.updated_at = admin_user_seed['updated_at']
    session.flush()


def sync_admin_user(session: Session) -> None:
    _upsert_admin_user(session)
    session.commit()


def seed_database(session: Session) -> None:
    try:
        _upsert_admin_user(session)

        already_seeded = session.scalar(select(Project.id).limit(1))
        if already_seeded:
            session.commit()
            return

        session.add_all([NavigationItem(**_with_uuid_fields(item, 'id')) for item in NAVIGATION_ITEMS])

        media_models = []
        for item in MEDIA_FILES:
            media_payload = _with_uuid_fields(item, 'id', 'uploaded_by_id')
            media_payload['visibility'] = MediaVisibility(media_payload['visibility'])
            media_payload['created_at'] = _parse_datetime(media_payload.get('created_at')) or TIMESTAMP
            media_payload['updated_at'] = _parse_datetime(media_payload.get('updated_at')) or TIMESTAMP
            media_models.append(MediaFile(**media_payload))
        session.add_all(media_models)

        session.add_all([SkillCategory(**_with_uuid_fields(item, 'id')) for item in SKILL_CATEGORIES])

        skill_models = []
        for item in SKILLS:
            skill_payload = _with_uuid_fields(item, 'id', 'category_id')
            skill_payload['created_at'] = _parse_datetime(skill_payload.get('created_at')) or TIMESTAMP
            skill_models.append(Skill(**skill_payload))
        session.add_all(skill_models)

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

        experience_models = []
        for item in EXPERIENCES:
            experience_payload = _with_uuid_fields(item, 'id', 'logo_file_id')
            experience_payload['start_date'] = _parse_date(experience_payload.get('start_date'))
            experience_payload['end_date'] = _parse_date(experience_payload.get('end_date'))
            experience_payload['created_at'] = _parse_datetime(experience_payload.get('created_at')) or TIMESTAMP
            experience_payload['updated_at'] = _parse_datetime(experience_payload.get('updated_at')) or TIMESTAMP
            experience_models.append(Experience(**experience_payload))
        session.add_all(experience_models)

        session.add_all([
            GithubContributionDay(**_with_uuid_fields(item, 'id', 'snapshot_id'))
            for item in CONTRIBUTION_DAYS
        ])

        session.add_all([
            SiteEvent(**_with_uuid_fields(item, 'id'))
            for item in SITE_EVENT_ROWS
        ])
        session.flush()

        session.add_all([
            ExperienceSkill(experience_id=seed_uuid(experience_id), skill_id=seed_uuid(skill_id))
            for experience_id, skill_id in EXPERIENCE_SKILLS
        ])
        session.flush()

        skill_name_to_id = {skill['name']: seed_uuid(skill['id']) for skill in SKILLS}
        for project in PROJECT_ROWS:
            github_owner = None
            if project.get('github_url') and 'github.com/' in project['github_url']:
                github_owner = project['github_url'].rstrip('/').split('/')[-2] if '/' in project['github_url'].rstrip('/') else None
                if github_owner == 'github.com':
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
