from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.domains.admin.repository.stats import AdminGithubRepository
from app.domains.admin.schema import AdminGithubSnapshotOut
from app.domains.github.sync import GithubStatsSyncError, GithubStatsSyncService


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
