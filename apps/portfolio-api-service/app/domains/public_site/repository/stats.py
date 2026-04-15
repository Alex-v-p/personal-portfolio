from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.db.models import BlogPost, EventType, Experience, GithubSnapshot, Project, ProjectState, PublicationStatus, SiteEvent, Skill
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
        page_view_count = self.session.scalar(select(func.count(SiteEvent.id)).where(SiteEvent.event_type == EventType.PAGE_VIEW)) or 0
        portfolio_like_count = self.session.scalar(select(func.count(SiteEvent.id)).where(SiteEvent.event_type == EventType.PORTFOLIO_LIKE)) or 0

        snapshot = self.get_latest_github_snapshot()
        contribution_days = snapshot.contribution_days if snapshot else []
        anchor_date = date.fromisoformat(snapshot.snapshot_date) if snapshot and snapshot.snapshot_date else None
        contribution_weeks = self._build_contribution_weeks(contribution_days, anchor_date=anchor_date)

        return StatsOut(
            contribution_weeks=contribution_weeks,
            github_summary=StatItemOut(
                id='github-public-repos',
                label='Public repos',
                value=str(snapshot.public_repo_count if snapshot and snapshot.public_repo_count is not None else 0),
                description='Public repositories currently visible on GitHub.',
                meta=f"{snapshot.username} · latest snapshot" if snapshot else 'No snapshot available',
                footnote=(
                    f"{snapshot.total_commits or 0} total commits"
                    if snapshot
                    else 'GitHub snapshot not available'
                ),
            ),
            latest_github_snapshot=snapshot,
            portfolio_highlights=[
                StatItemOut(
                    id='highlight-total-views',
                    label='Total views',
                    value=str(page_view_count),
                    description='Recorded public page views across the portfolio.',
                ),
                StatItemOut(
                    id='highlight-portfolio-likes',
                    label='Like counter',
                    value=str(portfolio_like_count),
                    description='Visitors who tapped the portfolio like button.',
                    action_label='Love this portfolio',
                ),
            ],
            portfolio_stats=[
                StatItemOut(id='stat-projects', label='Projects', value=str(project_count), description='Published portfolio projects.'),
                StatItemOut(id='stat-posts', label='Blog posts', value=str(blog_count), description='Posts available on the public blog.'),
                StatItemOut(id='stat-featured-projects', label='Featured projects', value=str(featured_project_count), description='Projects currently highlighted on the portfolio.'),
                StatItemOut(id='stat-featured-posts', label='Featured posts', value=str(featured_blog_count), description='Blog posts currently featured for discovery.'),
                StatItemOut(id='stat-skills', label='Skills', value=str(skill_count), description='Skills currently modeled in the portfolio.'),
                StatItemOut(id='stat-experience', label='Experience entries', value=str(experience_count), description='Experience timeline rows available publicly.'),
            ],
            month_labels=self._build_month_labels(contribution_days, anchor_date=anchor_date),
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

    def _build_contribution_weeks(
        self,
        days: list[GithubContributionDayOut],
        *,
        anchor_date: date | None = None,
    ) -> list[list[int]]:
        grid_start, grid_end = self._build_contribution_window(days, anchor_date=anchor_date)
        grouped: dict[date, int] = {date.fromisoformat(day.date): day.level for day in days}
        weeks: list[list[int]] = []
        current = grid_start
        while current <= grid_end:
            week: list[int] = []
            for _ in range(7):
                week.append(grouped.get(current, 0))
                current += timedelta(days=1)
            weeks.append(week)
        return weeks

    def _build_month_labels(
        self,
        days: list[GithubContributionDayOut],
        *,
        anchor_date: date | None = None,
    ) -> list[str]:
        grid_start, grid_end = self._build_contribution_window(days, anchor_date=anchor_date)
        labels: list[str] = []
        current = grid_start
        last_month: int | None = None
        while current <= grid_end:
            labels.append(current.strftime('%b') if current.month != last_month else '')
            last_month = current.month
            current += timedelta(days=7)
        return labels

    def _build_contribution_window(
        self,
        days: list[GithubContributionDayOut],
        *,
        anchor_date: date | None = None,
    ) -> tuple[date, date]:
        resolved_anchor = anchor_date
        if resolved_anchor is None and days:
            resolved_anchor = max(date.fromisoformat(day.date) for day in days)
        if resolved_anchor is None:
            resolved_anchor = date.today()

        window_start = resolved_anchor - timedelta(days=364)
        grid_start = window_start - timedelta(days=window_start.weekday())
        grid_end = resolved_anchor + timedelta(days=6 - resolved_anchor.weekday())
        return grid_start, grid_end
