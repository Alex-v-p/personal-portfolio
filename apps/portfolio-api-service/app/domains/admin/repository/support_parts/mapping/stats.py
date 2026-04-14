from __future__ import annotations

from app.db.models import GithubSnapshot
from app.domains.admin.schema import AdminGithubContributionDayOut, AdminGithubSnapshotOut
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.maintenance import MaintenanceJobStatus


class AdminRepositoryStatsMappingMixin:
    def _map_github_snapshot(
        self,
        snapshot: GithubSnapshot,
        *,
        auto_refresh_username: str | None,
        github_auto_refresh: 'MaintenanceJobStatus',
    ) -> AdminGithubSnapshotOut:
        ordered_days = sorted(snapshot.contribution_days, key=lambda day: day.contribution_date)
        username_matches_auto_refresh = bool(
            auto_refresh_username and snapshot.username.strip().lower() == auto_refresh_username.strip().lower()
        )

        return AdminGithubSnapshotOut(
            id=str(snapshot.id),
            snapshot_date=snapshot.snapshot_date.isoformat(),
            username=snapshot.username,
            public_repo_count=snapshot.public_repo_count,
            followers_count=snapshot.followers_count,
            following_count=snapshot.following_count,
            total_stars=snapshot.total_stars,
            total_commits=snapshot.total_commits,
            raw_payload=snapshot.raw_payload,
            contribution_days=[
                AdminGithubContributionDayOut(
                    date=day.contribution_date.isoformat(),
                    count=day.contribution_count,
                    level=day.level,
                )
                for day in ordered_days
            ],
            created_at=snapshot.created_at.isoformat(),
            updated_at=snapshot.created_at.isoformat(),
            auto_refresh_enabled=username_matches_auto_refresh and github_auto_refresh.enabled,
            auto_refresh_status=github_auto_refresh.status if username_matches_auto_refresh and github_auto_refresh.enabled else 'manual_only',
            next_auto_refresh_at=self._serialize_datetime(github_auto_refresh.next_run_at) if username_matches_auto_refresh and github_auto_refresh.enabled else None,
            seconds_until_auto_refresh=github_auto_refresh.seconds_until_next_run if username_matches_auto_refresh and github_auto_refresh.enabled else None,
        )
