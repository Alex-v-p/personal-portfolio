from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any
from urllib import parse

from app.core.config import get_settings
from app.services.github_stats.client import GithubHttpClient
from app.services.github_stats.contributions import GithubContributionSyncClient
from app.services.github_stats.models import GithubStatsSyncError, SyncedGithubContributionDay, SyncedGithubSnapshot


class GithubStatsSyncService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.http = GithubHttpClient()
        self.contributions = GithubContributionSyncClient()

    def sync_profile(self, username: str | None = None) -> SyncedGithubSnapshot:
        login = (username or self.settings.github_stats_username or '').strip()
        if not login:
            raise GithubStatsSyncError('No GitHub username configured for stats refresh.')

        user_payload = self.http.get_json(f'https://api.github.com/users/{parse.quote(login)}')
        repositories = self._list_public_repositories(login)
        contribution_days, contribution_meta = self._get_contribution_days(login)
        total_stars = sum(max(int(repo.get('stargazers_count') or 0), 0) for repo in repositories)
        total_contributions = sum(day.count for day in contribution_days)
        fetched_at = datetime.now(UTC).isoformat()
        raw_payload = {
            'fetchedAt': fetched_at,
            'source': contribution_meta.get('source', 'rest+scrape'),
            'user': {
                'login': user_payload.get('login'),
                'name': user_payload.get('name'),
                'htmlUrl': user_payload.get('html_url'),
                'publicRepos': user_payload.get('public_repos'),
                'followers': user_payload.get('followers'),
                'following': user_payload.get('following'),
                'avatarUrl': user_payload.get('avatar_url'),
            },
            'repositorySummary': {
                'count': len(repositories),
                'stars': total_stars,
            },
            'contributionSummary': {
                'count': total_contributions,
                'days': len(contribution_days),
                **contribution_meta,
            },
        }
        return SyncedGithubSnapshot(
            snapshot_date=date.today().isoformat(),
            username=str(user_payload.get('login') or login),
            public_repo_count=max(int(user_payload.get('public_repos') or len(repositories)), 0),
            followers_count=self._to_int_or_none(user_payload.get('followers')),
            following_count=self._to_int_or_none(user_payload.get('following')),
            total_stars=total_stars,
            total_commits=total_contributions,
            raw_payload=raw_payload,
            contribution_days=contribution_days,
        )

    def _list_public_repositories(self, username: str) -> list[dict[str, Any]]:
        repositories: list[dict[str, Any]] = []
        page = 1
        while True:
            query = parse.urlencode({'per_page': 100, 'page': page, 'type': 'owner', 'sort': 'updated'})
            payload = self.http.get_json(f'https://api.github.com/users/{parse.quote(username)}/repos?{query}')
            if not isinstance(payload, list):
                raise GithubStatsSyncError('GitHub repository response had an unexpected shape.')
            repositories.extend([item for item in payload if isinstance(item, dict)])
            if len(payload) < 100:
                break
            page += 1
            if page > 10:
                break
        return repositories

    def _get_contribution_days(self, username: str) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
        from_date = (date.today() - timedelta(days=max(self.settings.github_stats_lookback_days - 1, 0))).isoformat()
        to_date = date.today().isoformat()
        token = self.settings.github_api_token.strip()
        if token:
            try:
                return self.contributions.fetch_graphql(username=username, from_date=from_date, to_date=to_date)
            except GithubStatsSyncError:
                pass
        return self.contributions.fetch_public(
            username=username,
            from_date=from_date,
            to_date=to_date,
            html_fetcher=lambda url: self.http.get_text(url, accept='image/svg+xml,text/html'),
        )

    @staticmethod
    def _to_int_or_none(value: Any) -> int | None:
        if value is None:
            return None
        try:
            return max(int(value), 0)
        except (TypeError, ValueError):
            return None
