from __future__ import annotations

from app.schemas.base import ApiSchema


class StatItemOut(ApiSchema):
    id: str
    label: str
    value: str
    description: str
    action_label: str | None = None
    meta: str | None = None
    footnote: str | None = None


class GithubContributionDayOut(ApiSchema):
    date: str
    count: int
    level: int


class GithubSnapshotOut(ApiSchema):
    id: str
    snapshot_date: str
    username: str
    public_repo_count: int
    followers_count: int | None = None
    following_count: int | None = None
    total_stars: int | None = None
    total_commits: int | None = None
    created_at: str
    contribution_days: list[GithubContributionDayOut]


class StatsOut(ApiSchema):
    contribution_weeks: list[list[int]]
    github_summary: StatItemOut
    latest_github_snapshot: GithubSnapshotOut | None = None
    portfolio_highlights: list[StatItemOut]
    portfolio_stats: list[StatItemOut]
    month_labels: list[str]
    weekday_labels: list[str]


__all__ = ['GithubContributionDayOut', 'GithubSnapshotOut', 'StatItemOut', 'StatsOut']
