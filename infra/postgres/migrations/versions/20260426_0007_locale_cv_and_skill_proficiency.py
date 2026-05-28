"""add localized resumes and skill proficiency labels

Revision ID: 20260426_0007
Revises: 20260422_0006
Create Date: 2026-04-26 12:30:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = '20260426_0007'
down_revision = '20260422_0006'
branch_labels = None
depends_on = None


def _is_sqlite() -> bool:
    return op.get_bind().dialect.name == 'sqlite'


def upgrade() -> None:
    op.add_column('profiles', sa.Column('resume_file_id_nl', sa.Uuid(), nullable=True))
    # SQLite cannot add foreign-key constraints to an existing table with ALTER TABLE.
    # The test suite runs migrations against SQLite, while production uses Postgres.
    if not _is_sqlite():
        op.create_foreign_key(
            'fk_profiles_resume_file_id_nl_media_files',
            'profiles',
            'media_files',
            ['resume_file_id_nl'],
            ['id'],
            ondelete='SET NULL',
        )

    op.add_column('skills', sa.Column('proficiency_label', sa.String(length=80), nullable=True))
    op.add_column('skills', sa.Column('proficiency_label_nl', sa.String(length=80), nullable=True))

    profiles_table = sa.table(
        'profiles',
        sa.column('resume_file_id', sa.Uuid()),
        sa.column('resume_file_id_nl', sa.Uuid()),
    )
    op.execute(
        profiles_table.update()
        .where(sa.and_(profiles_table.c.resume_file_id.is_not(None), profiles_table.c.resume_file_id_nl.is_(None)))
        .values(resume_file_id_nl=profiles_table.c.resume_file_id)
    )

    skills_table = sa.table(
        'skills',
        sa.column('name', sa.String(length=120)),
        sa.column('proficiency_label', sa.String(length=80)),
        sa.column('proficiency_label_nl', sa.String(length=80)),
    )
    language_defaults = {
        'Dutch': ('Native', 'Moedertaal'),
        'English': ('C1 · Professional working proficiency', 'C1 · Professionele werkvaardigheid'),
        'Portuguese': ('Learning', 'Aan het leren'),
    }
    for name, (label, label_nl) in language_defaults.items():
        op.execute(
            skills_table.update()
            .where(
                sa.and_(
                    skills_table.c.name == name,
                    sa.or_(skills_table.c.proficiency_label.is_(None), skills_table.c.proficiency_label == ''),
                )
            )
            .values(proficiency_label=label, proficiency_label_nl=label_nl)
        )


def downgrade() -> None:
    op.drop_column('skills', 'proficiency_label_nl')
    op.drop_column('skills', 'proficiency_label')
    if not _is_sqlite():
        op.drop_constraint('fk_profiles_resume_file_id_nl_media_files', 'profiles', type_='foreignkey')
    op.drop_column('profiles', 'resume_file_id_nl')
