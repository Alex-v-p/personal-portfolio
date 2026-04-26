from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any
from urllib import parse

from app.core.config import get_settings
from app.domains.github.service.client import GithubHttpClient
from app.domains.github.service.contributions import GithubContributionSyncClient
from app.domains.github.service.models import GithubStatsSyncError, SyncedGithubContributionDay, SyncedGithubSnapshot


class GithubStatsSyncService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.http = GithubHttpClient()
        self.contributions = GithubContributionSyncClient()

    def sync_profile(self, username: str | None = None) -> SyncedGithubSnapshot:
        login = (username or self.settings.github_stats_username or '').strip()
        if not login:
            raise GithubStatsSyncError('No GitHub username configured for stats refresh.')

        profile_warning: str | None = None
        try:
            user_payload = self.http.get_json(f'https://api.github.com/users/{parse.quote(login)}')
        except GithubStatsSyncError as exc:
            if not self.settings.github_api_token.strip():
                raise
            profile_warning = str(exc)
            user_payload = self.http.get_json(f'https://api.github.com/users/{parse.quote(login)}', use_token=False)

        repositories, repository_warning = self._list_public_repositories(login)
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
        if profile_warning:
            raw_payload['profileWarning'] = 'Token-backed REST user lookup failed; refreshed the public profile data without the token instead.'
            raw_payload['profileWarningDetail'] = profile_warning
        if repository_warning:
            raw_payload['repositoryWarning'] = 'Token-backed REST repository lookup failed; refreshed public repository data without the token instead.'
            raw_payload['repositoryWarningDetail'] = repository_warning
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

    def _list_public_repositories(self, username: str) -> tuple[list[dict[str, Any]], str | None]:
        try:
            return self._list_public_repositories_with_auth_mode(username, use_token=True), None
        except GithubStatsSyncError as exc:
            if not self.settings.github_api_token.strip():
                raise
            return self._list_public_repositories_with_auth_mode(username, use_token=False), str(exc)

    def _list_public_repositories_with_auth_mode(self, username: str, *, use_token: bool) -> list[dict[str, Any]]:
        repositories: list[dict[str, Any]] = []
        page = 1
        while True:
            query = parse.urlencode({'per_page': 100, 'page': page, 'type': 'owner', 'sort': 'updated'})
            payload = self.http.get_json(f'https://api.github.com/users/{parse.quote(username)}/repos?{query}', use_token=use_token)
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
        graphql_error: str | None = None

        if token:
            try:
                return self.contributions.fetch_graphql(username=username, from_date=from_date, to_date=to_date)
            except GithubStatsSyncError as exc:
                graphql_error = str(exc)

        public_accept_header = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/svg+xml;q=0.8,*/*;q=0.7'
        try:
            contribution_days, contribution_meta = self.contributions.fetch_public(
                username=username,
                from_date=from_date,
                to_date=to_date,
                svg_fetcher=lambda url: self.http.get_text(url, accept=public_accept_header),
                html_fetcher=lambda url: self.http.get_text(url, accept=public_accept_header),
            )
        except GithubStatsSyncError as exc:
            if graphql_error:
                raise GithubStatsSyncError(
                    f'GitHub token GraphQL refresh failed ({graphql_error}). Public contribution scraping fallback also failed ({exc}). Check that GITHUB_API_TOKEN is valid, the username is correct, and the profile contribution graph is accessible.'
                ) from exc
            raise

        if graphql_error:
            contribution_meta = {
                **contribution_meta,
                'graphqlWarning': graphql_error,
                'warning': 'GraphQL contribution sync failed, so the refresh used public profile scraping as a fallback.',
            }

        return contribution_days, contribution_meta

    @staticmethod
    def _to_int_or_none(value: Any) -> int | None:
        if value is None:
            return None
        try:
            return max(int(value), 0)
        except (TypeError, ValueError):
            return None
