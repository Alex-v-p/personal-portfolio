from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.db.models import BlogPost, Experience, GithubSnapshot, Project, ProjectState, PublicationStatus, Skill
from app.domains.public_site.schema import GithubContributionDayOut, GithubSnapshotOut, StatItemOut, StatsOut


class PublicStatsRepositoryMixin:
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
        project_count = self.session.scalar(
            select(func.count(Project.id)).where(
                Project.state != ProjectState.ARCHIVED,
                Project.published_at <= self._publication_cutoff(),
            )
        ) or 0
        blog_count = self.session.scalar(
            select(func.count(BlogPost.id)).where(
                BlogPost.status == PublicationStatus.PUBLISHED,
                BlogPost.published_at.is_not(None),
                BlogPost.published_at <= self._publication_cutoff(),
            )
        ) or 0
        skill_count = self.session.scalar(select(func.count(Skill.id))) or 0
        featured_project_count = self.session.scalar(
            select(func.count(Project.id)).where(
                Project.is_featured.is_(True),
                Project.state != ProjectState.ARCHIVED,
                Project.published_at <= self._publication_cutoff(),
            )
        ) or 0
        featured_blog_count = self.session.scalar(
            select(func.count(BlogPost.id)).where(
                BlogPost.is_featured.is_(True),
                BlogPost.status == PublicationStatus.PUBLISHED,
                BlogPost.published_at.is_not(None),
                BlogPost.published_at <= self._publication_cutoff(),
            )
        ) or 0
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
