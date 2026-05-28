from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.db.models import GithubContributionDay, GithubSnapshot
from app.domains.admin.schema import AdminGithubSnapshotOut, AdminGithubSnapshotsListOut, AdminGithubSnapshotUpsertIn
from app.domains.admin.repository.support import AdminRepositorySupport
from app.domains.github.sync import SyncedGithubSnapshot
from app.services.maintenance import MaintenanceJobInspector


class AdminGithubRepository(AdminRepositorySupport):
    def list_github_snapshots(self) -> AdminGithubSnapshotsListOut:
        effective_now = datetime.now(UTC)
        auto_refresh_username = self.settings.github_stats_username.strip() or None
        github_auto_refresh = MaintenanceJobInspector(settings=self.settings).github_auto_refresh_status(now=effective_now)

        snapshots = self.session.scalars(
            select(GithubSnapshot)
            .options(selectinload(GithubSnapshot.contribution_days))
            .order_by(GithubSnapshot.snapshot_date.desc(), GithubSnapshot.created_at.desc())
        ).all()
        items = [
            self._map_github_snapshot(
                snapshot,
                auto_refresh_username=auto_refresh_username,
                github_auto_refresh=github_auto_refresh,
            )
            for snapshot in snapshots
        ]
        return AdminGithubSnapshotsListOut(
            items=items,
            total=len(items),
            auto_refresh_enabled=github_auto_refresh.enabled,
            auto_refresh_username=auto_refresh_username,
            auto_refresh_interval_seconds=self.settings.github_auto_refresh_interval_seconds,
            auto_refresh_retry_interval_seconds=self.settings.github_auto_refresh_retry_interval_seconds,
            auto_refresh_status=github_auto_refresh.status,
            next_auto_refresh_at=self._serialize_datetime(github_auto_refresh.next_run_at),
            seconds_until_auto_refresh=github_auto_refresh.seconds_until_next_run,
            last_auto_refresh_at=self._serialize_datetime(github_auto_refresh.last_success_at),
            last_auto_refresh_failed_at=self._serialize_datetime(github_auto_refresh.last_failed_at),
            auto_refresh_error=github_auto_refresh.last_error,
        )

    def get_github_snapshot(self, snapshot_id: UUID) -> AdminGithubSnapshotOut | None:
        auto_refresh_username = self.settings.github_stats_username.strip() or None
        github_auto_refresh = MaintenanceJobInspector(settings=self.settings).github_auto_refresh_status(now=datetime.now(UTC))
        snapshot = self.session.scalar(
            select(GithubSnapshot)
            .options(selectinload(GithubSnapshot.contribution_days))
            .where(GithubSnapshot.id == snapshot_id)
        )
        return self._map_github_snapshot(snapshot, auto_refresh_username=auto_refresh_username, github_auto_refresh=github_auto_refresh) if snapshot else None

    def create_github_snapshot(self, payload: AdminGithubSnapshotUpsertIn) -> AdminGithubSnapshotOut:
        snapshot = GithubSnapshot(
            snapshot_date=self._parse_date(payload.snapshot_date) or date.today(),
            username=payload.username.strip(),
            public_repo_count=payload.public_repo_count,
            followers_count=payload.followers_count,
            following_count=payload.following_count,
            total_stars=payload.total_stars,
            total_commits=payload.total_commits,
            raw_payload=payload.raw_payload,
        )
        self.session.add(snapshot)
        self.session.flush()
        self._replace_github_contribution_days(snapshot, payload)
        self.session.commit()
        return self.get_github_snapshot(snapshot.id)  # type: ignore[return-value]

    def update_github_snapshot(self, snapshot_id: UUID, payload: AdminGithubSnapshotUpsertIn) -> AdminGithubSnapshotOut | None:
        snapshot = self.session.get(GithubSnapshot, snapshot_id)
        if snapshot is None:
            return None
        snapshot.snapshot_date = self._parse_date(payload.snapshot_date) or snapshot.snapshot_date
        snapshot.username = payload.username.strip()
        snapshot.public_repo_count = payload.public_repo_count
        snapshot.followers_count = payload.followers_count
        snapshot.following_count = payload.following_count
        snapshot.total_stars = payload.total_stars
        snapshot.total_commits = payload.total_commits
        snapshot.raw_payload = payload.raw_payload
        self._replace_github_contribution_days(snapshot, payload)
        self.session.commit()
        return self.get_github_snapshot(snapshot_id)

    def delete_github_snapshot(self, snapshot_id: UUID) -> bool:
        snapshot = self.session.get(GithubSnapshot, snapshot_id)
        if snapshot is None:
            return False
        self.session.delete(snapshot)
        self.session.commit()
        return True

    def refresh_github_snapshot(self, synced_snapshot: SyncedGithubSnapshot, *, prune_history: bool = True) -> AdminGithubSnapshotOut:
        latest_snapshot = self.session.scalar(
            select(GithubSnapshot)
            .options(selectinload(GithubSnapshot.contribution_days))
            .where(func.lower(GithubSnapshot.username) == synced_snapshot.username.strip().lower())
            .order_by(GithubSnapshot.snapshot_date.desc(), GithubSnapshot.created_at.desc())
        )

        if latest_snapshot is None:
            latest_snapshot = GithubSnapshot(
                snapshot_date=self._parse_date(synced_snapshot.snapshot_date) or date.today(),
                username=synced_snapshot.username.strip(),
                public_repo_count=synced_snapshot.public_repo_count,
                followers_count=synced_snapshot.followers_count,
                following_count=synced_snapshot.following_count,
                total_stars=synced_snapshot.total_stars,
                total_commits=synced_snapshot.total_commits,
                raw_payload=synced_snapshot.raw_payload,
            )
            self.session.add(latest_snapshot)
            self.session.flush()
        else:
            latest_snapshot.snapshot_date = self._parse_date(synced_snapshot.snapshot_date) or latest_snapshot.snapshot_date
            latest_snapshot.username = synced_snapshot.username.strip()
            latest_snapshot.public_repo_count = synced_snapshot.public_repo_count
            latest_snapshot.followers_count = synced_snapshot.followers_count
            latest_snapshot.following_count = synced_snapshot.following_count
            latest_snapshot.total_stars = synced_snapshot.total_stars
            latest_snapshot.total_commits = synced_snapshot.total_commits
            latest_snapshot.raw_payload = synced_snapshot.raw_payload

        latest_snapshot.contribution_days.clear()
        self.session.flush()
        for day in synced_snapshot.contribution_days:
            latest_snapshot.contribution_days.append(
                GithubContributionDay(
                    contribution_date=self._parse_date(day.date) or date.today(),
                    contribution_count=day.count,
                    level=day.level,
                )
            )
        self.session.flush()

        if prune_history:
            obsolete_snapshots = self.session.scalars(
                select(GithubSnapshot).where(
                    func.lower(GithubSnapshot.username) == synced_snapshot.username.strip().lower(),
                    GithubSnapshot.id != latest_snapshot.id,
                )
            ).all()
            for snapshot in obsolete_snapshots:
                self.session.delete(snapshot)

        self.session.commit()
        return self.get_github_snapshot(latest_snapshot.id)  # type: ignore[return-value]
