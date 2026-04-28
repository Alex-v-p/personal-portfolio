from __future__ import annotations

from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from typing import Any
from urllib import parse

from app.core.config import get_settings
from app.domains.github.service.client import GithubHttpClient
from app.domains.github.service.contributions import GithubContributionSyncClient, level_from_count
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
        contribution_days, contribution_meta = self._get_contribution_days(login, repositories=repositories)
        total_stars = sum(max(int(repo.get('stargazers_count') or 0), 0) for repo in repositories)
        total_contributions = sum(day.count for day in contribution_days)
        fetched_at = datetime.now(UTC).isoformat()
        raw_payload = {
            'fetchedAt': fetched_at,
            'source': contribution_meta.get('source', 'rest-repository-commits'),
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

    def _get_contribution_days(self, username: str, *, repositories: list[dict[str, Any]]) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
        from_date = (date.today() - timedelta(days=max(self.settings.github_stats_lookback_days - 1, 0))).isoformat()
        to_date = date.today().isoformat()
        token = self.settings.github_api_token.strip()
        graphql_error: str | None = None
        rest_commit_error: str | None = None

        if token:
            try:
                return self.contributions.fetch_graphql(username=username, from_date=from_date, to_date=to_date)
            except GithubStatsSyncError as exc:
                graphql_error = str(exc)

        # Prefer the REST commit fallback over the public profile graph scraper. The public
        # /users/<name>/contributions SVG can silently collapse to a calendar-year slice, while
        # repo commit endpoints support an explicit rolling since/until window.
        try:
            contribution_days, contribution_meta = self._fetch_repository_commit_days(
                username=username,
                repositories=repositories,
                from_date=from_date,
                to_date=to_date,
            )
        except GithubStatsSyncError as exc:
            rest_commit_error = str(exc)
        else:
            if graphql_error:
                contribution_meta = {
                    **contribution_meta,
                    'graphqlWarning': graphql_error,
                    'warning': 'GraphQL contribution sync failed, so the refresh counted public repository commits through the REST API fallback.',
                }
            return contribution_days, contribution_meta

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
            details = []
            if graphql_error:
                details.append(f'GraphQL failed: {graphql_error}')
            if rest_commit_error:
                details.append(f'REST commit fallback failed: {rest_commit_error}')
            details.append(f'public contribution scrape failed: {exc}')
            raise GithubStatsSyncError(
                'GitHub stats refresh could not build the rolling contribution board. '
                + ' | '.join(details)
                + ' Check that GITHUB_API_TOKEN is valid or that public repository commits are accessible.'
            ) from exc

        if graphql_error or rest_commit_error:
            contribution_meta = {
                **contribution_meta,
                'graphqlWarning': graphql_error,
                'restCommitWarning': rest_commit_error,
                'warning': 'GraphQL and/or REST commit sync failed, so the refresh used public profile scraping as a final fallback.',
            }

        return contribution_days, contribution_meta

    def _fetch_repository_commit_days(
        self,
        *,
        username: str,
        repositories: list[dict[str, Any]],
        from_date: str,
        to_date: str,
    ) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
        window_start = date.fromisoformat(from_date)
        window_end = date.fromisoformat(to_date)
        if window_end < window_start:
            raise GithubStatsSyncError('GitHub commit sync received an invalid date window.')

        counts: defaultdict[date, int] = defaultdict(int)
        repo_count = 0
        skipped_repositories: list[str] = []
        accessible_repositories = 0
        repositories_with_commits = 0
        since = f'{from_date}T00:00:00Z'
        until = f'{to_date}T23:59:59Z'

        for repo in repositories:
            full_name = self._repo_full_name(repo)
            if not full_name:
                continue

            repo_count += 1
            encoded_full_name = '/'.join(parse.quote(part, safe='') for part in full_name.split('/', 1))
            page = 1
            repo_had_visible_commits = False
            repo_was_accessible = False
            while True:
                query = parse.urlencode(
                    {
                        'per_page': 100,
                        'page': page,
                        'since': since,
                        'until': until,
                        'author': username,
                    }
                )
                url = f'https://api.github.com/repos/{encoded_full_name}/commits?{query}'
                try:
                    payload = self.http.get_json(url)
                except GithubStatsSyncError as exc:
                    message = str(exc)
                    if 'HTTP 409' in message or 'Git Repository is empty' in message:
                        repo_was_accessible = True
                    else:
                        skipped_repositories.append(f'{full_name}: {message}')
                    break

                if not isinstance(payload, list):
                    skipped_repositories.append(f'{full_name}: unexpected commits response shape')
                    break

                repo_was_accessible = True
                if payload:
                    repo_had_visible_commits = True

                for item in payload:
                    commit_date = self._commit_author_date(item)
                    if commit_date is None or commit_date < window_start or commit_date > window_end:
                        continue
                    counts[commit_date] += 1

                if len(payload) < 100:
                    break
                page += 1
                if page > 50:
                    skipped_repositories.append(f'{full_name}: stopped after 5000 commits in the requested window')
                    break

            if repo_was_accessible:
                accessible_repositories += 1
            if repo_had_visible_commits:
                repositories_with_commits += 1

        if repo_count == 0:
            raise GithubStatsSyncError('No public repositories were available for the REST commit fallback.')

        # A no-commit year is a valid result, so return a zero-filled board as long as at least
        # one repository was accessible. Only fail when every repository request was blocked.
        if accessible_repositories == 0:
            raise GithubStatsSyncError('All public repository commit requests failed. ' + ' | '.join(skipped_repositories[:8]))

        contribution_days: list[SyncedGithubContributionDay] = []
        cursor = window_start
        while cursor <= window_end:
            count = max(counts.get(cursor, 0), 0)
            contribution_days.append(
                SyncedGithubContributionDay(
                    date=cursor.isoformat(),
                    count=count,
                    level=level_from_count(count),
                )
            )
            cursor += timedelta(days=1)

        meta: dict[str, Any] = {
            'source': 'rest-repository-commits',
            'from': from_date,
            'to': to_date,
            'totalContributions': sum(day.count for day in contribution_days),
            'days': len(contribution_days),
            'repositoryCount': repo_count,
            'accessibleRepositoryCount': accessible_repositories,
            'repositoriesWithCommits': repositories_with_commits,
        }
        if skipped_repositories:
            meta['repositoryWarnings'] = skipped_repositories[:12]
        return contribution_days, meta

    @staticmethod
    def _repo_full_name(repo: dict[str, Any]) -> str | None:
        full_name = repo.get('full_name')
        if isinstance(full_name, str) and '/' in full_name:
            return full_name

        owner = repo.get('owner')
        owner_login = owner.get('login') if isinstance(owner, dict) else None
        name = repo.get('name')
        if isinstance(owner_login, str) and isinstance(name, str) and owner_login.strip() and name.strip():
            return f'{owner_login}/{name}'
        return None

    @staticmethod
    def _commit_author_date(item: Any) -> date | None:
        if not isinstance(item, dict):
            return None
        commit = item.get('commit')
        if not isinstance(commit, dict):
            return None
        author = commit.get('author')
        committer = commit.get('committer')
        raw_date = None
        if isinstance(author, dict):
            raw_date = author.get('date')
        if not raw_date and isinstance(committer, dict):
            raw_date = committer.get('date')
        if not isinstance(raw_date, str) or len(raw_date) < 10:
            return None
        try:
            return date.fromisoformat(raw_date[:10])
        except ValueError:
            return None

    @staticmethod
    def _to_int_or_none(value: Any) -> int | None:
        if value is None:
            return None
        try:
            return max(int(value), 0)
        except (TypeError, ValueError):
            return None
