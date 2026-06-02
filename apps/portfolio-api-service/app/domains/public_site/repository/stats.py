from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.db.models import BlogPost, EventType, Experience, GithubSnapshot, Project, ProjectState, PublicationStatus, SiteEvent, Skill
from app.domains.public_site.schema import GithubContributionDayOut, GithubSnapshotOut, StatItemOut, StatsOut


_MONTH_LABELS = {
    'en': ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'nl': ['', 'jan', 'feb', 'mrt', 'apr', 'mei', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'],
}

_WEEKDAY_LABELS = {
    'en': ['Mon', '', 'Wed', '', 'Fri', '', ''],
    'nl': ['ma', '', 'wo', '', 'vr', '', ''],
}


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
        unique_page_viewer_count = self._count_unique_page_viewers()
        portfolio_like_count = self.session.scalar(select(func.count(SiteEvent.id)).where(SiteEvent.event_type == EventType.PORTFOLIO_LIKE)) or 0

        snapshot = self.get_latest_github_snapshot()
        contribution_days = snapshot.contribution_days if snapshot else []
        anchor_date = date.fromisoformat(snapshot.snapshot_date) if snapshot and snapshot.snapshot_date else None
        contribution_weeks = self._build_contribution_weeks(contribution_days, anchor_date=anchor_date)

        return StatsOut(
            contribution_weeks=contribution_weeks,
            github_summary=StatItemOut(
                id='github-public-repos',
                label=self._copy('stats_label_public_repos'),
                value=str(snapshot.public_repo_count if snapshot and snapshot.public_repo_count is not None else 0),
                description=self._copy('stats_description_public_repos'),
                meta=self._copy('stats_meta_latest_snapshot').format(username=snapshot.username) if snapshot else self._copy('stats_meta_no_snapshot'),
                footnote=(
                    self._copy('stats_footnote_total_commits').format(count=snapshot.total_commits or 0)
                    if snapshot
                    else self._copy('stats_footnote_github_unavailable')
                ),
            ),
            latest_github_snapshot=snapshot,
            portfolio_highlights=[
                StatItemOut(
                    id='highlight-total-views',
                    label=self._copy('stats_label_unique_views'),
                    value=str(unique_page_viewer_count),
                    description=self._copy('stats_description_unique_views'),
                ),
                StatItemOut(
                    id='highlight-portfolio-likes',
                    label=self._copy('stats_label_likes'),
                    value=str(portfolio_like_count),
                    description=self._copy('stats_description_likes'),
                    action_label=self._copy('stats_action_like'),
                ),
            ],
            portfolio_stats=[
                StatItemOut(id='stat-projects', label=self._copy('stats_label_projects'), value=str(project_count), description=self._copy('stats_description_projects')),
                StatItemOut(id='stat-posts', label=self._copy('stats_label_posts'), value=str(blog_count), description=self._copy('stats_description_posts')),
                StatItemOut(id='stat-featured-projects', label=self._copy('stats_label_featured_projects'), value=str(featured_project_count), description=self._copy('stats_description_featured_projects')),
                StatItemOut(id='stat-featured-posts', label=self._copy('stats_label_featured_posts'), value=str(featured_blog_count), description=self._copy('stats_description_featured_posts')),
                StatItemOut(id='stat-skills', label=self._copy('stats_label_skills'), value=str(skill_count), description=self._copy('stats_description_skills')),
                StatItemOut(id='stat-experience', label=self._copy('stats_label_experience'), value=str(experience_count), description=self._copy('stats_description_experience')),
            ],
            month_labels=self._build_month_labels(contribution_days, anchor_date=anchor_date),
            weekday_labels=self._localized_weekday_labels(),
        )

    def _count_unique_page_viewers(self) -> int:
        rows = self.session.execute(
            select(SiteEvent.visitor_id, SiteEvent.session_id, SiteEvent.metadata_json).where(SiteEvent.event_type == EventType.PAGE_VIEW)
        ).all()
        identities = {self._page_viewer_identity(visitor_id, session_id, metadata) for visitor_id, session_id, metadata in rows}
        return len(identities)

    def _page_viewer_identity(self, visitor_id: str | None, session_id: str | None, metadata: dict[str, Any] | None) -> str:
        normalized_visitor = self._normalize_identity_part(visitor_id)
        if normalized_visitor and normalized_visitor != 'anonymous':
            return f'visitor:{normalized_visitor}'

        normalized_session = self._normalize_identity_part(session_id)
        if normalized_session:
            return f'session:{normalized_session}'

        ip_address = metadata.get('ip_address') if isinstance(metadata, dict) else None
        normalized_ip = self._normalize_identity_part(ip_address)
        if normalized_ip:
            return f'ip:{normalized_ip}'

        return 'anonymous'

    @staticmethod
    def _normalize_identity_part(value: object) -> str:
        return str(value or '').strip()[:255]

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
            labels.append(self._localized_month_label(current.month) if current.month != last_month else '')
            last_month = current.month
            current += timedelta(days=7)
        return labels

    def _localized_month_label(self, month: int) -> str:
        labels = _MONTH_LABELS.get(self.locale, _MONTH_LABELS['en'])
        return labels[month] if 0 < month < len(labels) else ''

    def _localized_weekday_labels(self) -> list[str]:
        return _WEEKDAY_LABELS.get(self.locale, _WEEKDAY_LABELS['en'])

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
