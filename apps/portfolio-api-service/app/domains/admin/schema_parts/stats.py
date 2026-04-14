from __future__ import annotations

from typing import Any

from pydantic import Field

from app.schemas.base import ApiSchema


class AdminGithubContributionDayIn(ApiSchema):
    date: str
    count: int = Field(ge=0)
    level: int = Field(ge=0)


class AdminGithubContributionDayOut(ApiSchema):
    date: str
    count: int
    level: int


class AdminGithubSnapshotUpsertIn(ApiSchema):
    snapshot_date: str
    username: str = Field(min_length=1, max_length=120)
    public_repo_count: int = Field(ge=0)
    followers_count: int | None = Field(default=None, ge=0)
    following_count: int | None = Field(default=None, ge=0)
    total_stars: int | None = Field(default=None, ge=0)
    total_commits: int | None = Field(default=None, ge=0)
    raw_payload: dict[str, Any] | None = None
    contribution_days: list[AdminGithubContributionDayIn] = Field(default_factory=list)


class AdminGithubSnapshotOut(ApiSchema):
    id: str
    snapshot_date: str
    username: str
    public_repo_count: int
    followers_count: int | None = None
    following_count: int | None = None
    total_stars: int | None = None
    total_commits: int | None = None
    raw_payload: dict[str, Any] | None = None
    contribution_days: list[AdminGithubContributionDayOut]
    created_at: str
    updated_at: str


class AdminGithubSnapshotsListOut(ApiSchema):
    items: list[AdminGithubSnapshotOut]
    total: int


class AdminGithubSnapshotRefreshIn(ApiSchema):
    username: str | None = Field(default=None, max_length=120)
    prune_history: bool = True


__all__ = [
    'AdminGithubContributionDayIn',
    'AdminGithubContributionDayOut',
    'AdminGithubSnapshotOut',
    'AdminGithubSnapshotRefreshIn',
    'AdminGithubSnapshotsListOut',
    'AdminGithubSnapshotUpsertIn',
]
