from __future__ import annotations

from app.db.models import GithubSnapshot
from app.domains.admin.schema import AdminGithubContributionDayOut, AdminGithubSnapshotOut


class AdminRepositoryStatsMappingMixin:
    def _map_github_snapshot(self, snapshot: GithubSnapshot) -> AdminGithubSnapshotOut:
        ordered_days = sorted(snapshot.contribution_days, key=lambda day: day.contribution_date)

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
        )
