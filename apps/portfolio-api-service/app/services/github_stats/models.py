from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SyncedGithubContributionDay:
    date: str
    count: int
    level: int


@dataclass(slots=True)
class SyncedGithubSnapshot:
    snapshot_date: str
    username: str
    public_repo_count: int
    followers_count: int | None
    following_count: int | None
    total_stars: int | None
    total_commits: int | None
    raw_payload: dict[str, Any]
    contribution_days: list[SyncedGithubContributionDay]


class GithubStatsSyncError(RuntimeError):
    pass
