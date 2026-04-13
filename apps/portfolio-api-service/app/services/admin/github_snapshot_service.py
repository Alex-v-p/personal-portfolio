from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.admin.stats import AdminGithubRepository
from app.schemas.admin import AdminGithubSnapshotOut
from app.services.github_stats_sync import GithubStatsSyncError, GithubStatsSyncService


class AdminGithubSnapshotService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminGithubRepository(session)
        self.sync = GithubStatsSyncService()

    def refresh(self, username: str, *, prune_history: bool) -> AdminGithubSnapshotOut:
        try:
            synced = self.sync.sync_profile(username)
        except GithubStatsSyncError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        return self.repository.refresh_github_snapshot(synced, prune_history=prune_history)
