"""normalize legacy icon keys and backfill seeded defaults

Revision ID: 20260422_0006
Revises: 20260422_0005
Create Date: 2026-04-22 00:45:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260422_0006'
down_revision = '20260422_0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    skill_categories_table = sa.table(
        'skill_categories',
        sa.column('name', sa.String(length=120)),
        sa.column('icon_key', sa.String(length=80)),
    )
    category_defaults = {
        'Front-End': 'code',
        'Back-End': 'server',
        'Data & AI': 'brain',
        'Infrastructure & Tools': 'database',
        'Analysis & Collaboration': 'workflow',
        'Languages': 'languages',
    }
    for name, icon_key in category_defaults.items():
        op.execute(
            skill_categories_table.update()
            .where(
                sa.and_(
                    skill_categories_table.c.name == name,
                    sa.or_(
                        skill_categories_table.c.icon_key.is_(None),
                        skill_categories_table.c.icon_key == '',
                    ),
                )
            )
            .values(icon_key=icon_key)
        )

    social_links_table = sa.table(
        'social_links',
        sa.column('platform', sa.String(length=50)),
        sa.column('icon_key', sa.String(length=80)),
    )
    social_defaults = {
        'github': 'github',
        'linkedin': 'linkedin',
        'twitter': 'twitter',
        'instagram': 'instagram',
        'email': 'mail',
        'phone': 'phone',
        'location': 'map-pin',
        'portfolio': 'globe',
        'website': 'globe',
    }
    for platform, icon_key in social_defaults.items():
        op.execute(
            social_links_table.update()
            .where(
                sa.and_(
                    social_links_table.c.platform == platform,
                    sa.or_(
                        social_links_table.c.icon_key.is_(None),
                        social_links_table.c.icon_key == '',
                        social_links_table.c.icon_key.in_(['email', 'telephone', 'linked-in', 'world', 'website']),
                    ),
                )
            )
            .values(icon_key=icon_key)
        )

    skills_table = sa.table(
        'skills',
        sa.column('name', sa.String(length=120)),
        sa.column('icon_key', sa.String(length=80)),
    )

    legacy_icon_updates = {
        'tailwind': 'tailwindcss',
        'fastapi': 'server',
        'csharp': 'code',
        'pandas': 'database',
        'network': 'globe',
        'clipboard-search': 'workflow',
        'layout-template': 'workflow',
        'users': 'workflow',
    }
    for old_icon_key, new_icon_key in legacy_icon_updates.items():
        op.execute(
            skills_table.update()
            .where(skills_table.c.icon_key == old_icon_key)
            .values(icon_key=new_icon_key)
        )

    skill_defaults = {
        'Angular': 'angular',
        'Tailwind CSS': 'tailwindcss',
        'TypeScript': 'typescript',
        'Laravel': 'laravel',
        'FastAPI': 'server',
        'SQL': 'sql',
        'C#': 'code',
        'Python': 'python',
        'Machine Learning': 'brain',
        'Pandas': 'database',
        'Git': 'git',
        'Docker': 'docker',
        'Networking Basics': 'globe',
        'Proxmox': 'server',
        'Kubernetes': 'kubernetes',
        'Requirements Analysis': 'workflow',
        'UML': 'workflow',
        'Prototyping': 'workflow',
        'Team Leadership': 'workflow',
        'Dutch': 'languages',
        'English': 'languages',
        'Portuguese': 'languages',
    }
    for name, icon_key in skill_defaults.items():
        update_condition = sa.or_(
            skills_table.c.icon_key.is_(None),
            skills_table.c.icon_key == '',
        )
        if name == 'SQL':
            update_condition = sa.or_(update_condition, skills_table.c.icon_key == 'database')

        op.execute(
            skills_table.update()
            .where(sa.and_(skills_table.c.name == name, update_condition))
            .values(icon_key=icon_key)
        )


def downgrade() -> None:
    skills_table = sa.table(
        'skills',
        sa.column('name', sa.String(length=120)),
        sa.column('icon_key', sa.String(length=80)),
    )
    social_links_table = sa.table(
        'social_links',
        sa.column('platform', sa.String(length=50)),
        sa.column('icon_key', sa.String(length=80)),
    )

    reverted_skill_icons = {
        'Tailwind CSS': 'tailwind',
        'FastAPI': 'fastapi',
        'SQL': 'database',
        'C#': 'csharp',
        'Pandas': 'pandas',
        'Networking Basics': 'network',
        'Requirements Analysis': 'clipboard-search',
        'Prototyping': 'layout-template',
        'Team Leadership': 'users',
    }
    for name, icon_key in reverted_skill_icons.items():
        op.execute(
            skills_table.update()
            .where(skills_table.c.name == name)
            .values(icon_key=icon_key)
        )

    reverted_social_icons = {
        'email': 'email',
        'phone': 'telephone',
        'location': 'world',
        'portfolio': 'website',
    }
    for platform, icon_key in reverted_social_icons.items():
        op.execute(
            social_links_table.update()
            .where(social_links_table.c.platform == platform)
            .values(icon_key=icon_key)
        )
