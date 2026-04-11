from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
import json
import re
from typing import Any
from urllib import error, parse, request

from app.core.config import get_settings


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


_LEVEL_MAP = {
    'NONE': 0,
    'FIRST_QUARTILE': 1,
    'SECOND_QUARTILE': 2,
    'THIRD_QUARTILE': 3,
    'FOURTH_QUARTILE': 4,
}
_SVG_DAY_PATTERN = re.compile(
    r'data-date="(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})"[^>]*data-count="(?P<count>[0-9]+)"[^>]*data-level="(?P<level>[0-4])"'
)
_TOOLTIP_DAY_PATTERN = re.compile(
    r'(?P<count>[0-9]+) contribution[s]? on (?P<month>[A-Za-z]+) (?P<day>[0-9]{1,2})(?:st|nd|rd|th)'
)
_MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}


class GithubStatsSyncError(RuntimeError):
    pass


class GithubStatsSyncService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.api_version = '2022-11-28'

    def sync_profile(self, username: str | None = None) -> SyncedGithubSnapshot:
        login = (username or self.settings.github_stats_username or '').strip()
        if not login:
            raise GithubStatsSyncError('No GitHub username configured for stats refresh.')

        user_payload = self._get_json(f'https://api.github.com/users/{parse.quote(login)}')
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
            payload = self._get_json(f'https://api.github.com/users/{parse.quote(username)}/repos?{query}')
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
                return self._get_contribution_days_graphql(username=username, from_date=from_date, to_date=to_date)
            except GithubStatsSyncError:
                pass

        return self._get_contribution_days_public(username=username, from_date=from_date, to_date=to_date)

    def _get_contribution_days_graphql(self, *, username: str, from_date: str, to_date: str) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
        token = self.settings.github_api_token.strip()
        if not token:
            raise GithubStatsSyncError('GraphQL contribution sync requires a GitHub token.')

        query = '''
        query PortfolioGithubSnapshot($login: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $login) {
            contributionsCollection(from: $from, to: $to) {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    contributionCount
                    contributionLevel
                    date
                  }
                }
              }
            }
          }
        }
        '''
        body = json.dumps({
            'query': query,
            'variables': {
                'login': username,
                'from': f'{from_date}T00:00:00Z',
                'to': f'{to_date}T23:59:59Z',
            },
        }).encode('utf-8')
        req = request.Request(
            'https://api.github.com/graphql',
            data=body,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'User-Agent': 'portfolio-api-service',
            },
            method='POST',
        )
        try:
            with request.urlopen(req, timeout=20) as response:
                payload = json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore')
            raise GithubStatsSyncError(f'GitHub GraphQL request failed: {exc.code} {detail or exc.reason}') from exc
        except error.URLError as exc:
            raise GithubStatsSyncError(f'GitHub GraphQL request failed: {exc.reason}') from exc

        if payload.get('errors'):
            raise GithubStatsSyncError(f"GitHub GraphQL returned errors: {payload['errors']}")

        calendar = (((payload.get('data') or {}).get('user') or {}).get('contributionsCollection') or {}).get('contributionCalendar')
        if not isinstance(calendar, dict):
            raise GithubStatsSyncError('GitHub GraphQL contribution calendar was missing from the response.')

        contribution_days: list[SyncedGithubContributionDay] = []
        for week in calendar.get('weeks') or []:
            if not isinstance(week, dict):
                continue
            for day in week.get('contributionDays') or []:
                if not isinstance(day, dict):
                    continue
                contribution_days.append(
                    SyncedGithubContributionDay(
                        date=str(day.get('date')),
                        count=max(int(day.get('contributionCount') or 0), 0),
                        level=_LEVEL_MAP.get(str(day.get('contributionLevel') or 'NONE'), 0),
                    )
                )

        contribution_days.sort(key=lambda item: item.date)
        return contribution_days, {
            'source': 'graphql',
            'from': from_date,
            'to': to_date,
            'totalContributions': max(int(calendar.get('totalContributions') or 0), 0),
        }

    def _get_contribution_days_public(self, *, username: str, from_date: str, to_date: str) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
        query = parse.urlencode({'from': from_date, 'to': to_date})
        html = self._get_text(f'https://github.com/users/{parse.quote(username)}/contributions?{query}', accept='image/svg+xml,text/html')
        days = self._parse_svg_contribution_days(html)
        if not days:
            days = self._parse_tooltip_contribution_days(html, to_date=to_date)
        if not days:
            raise GithubStatsSyncError('GitHub contribution graph could not be parsed from the public profile response.')
        return days, {
            'source': 'public-profile',
            'from': from_date,
            'to': to_date,
            'totalContributions': sum(day.count for day in days),
        }

    def _parse_svg_contribution_days(self, html: str) -> list[SyncedGithubContributionDay]:
        days = [
            SyncedGithubContributionDay(
                date=match.group('date'),
                count=max(int(match.group('count')), 0),
                level=max(int(match.group('level')), 0),
            )
            for match in _SVG_DAY_PATTERN.finditer(html)
        ]
        days.sort(key=lambda item: item.date)
        return days

    def _parse_tooltip_contribution_days(self, html: str, *, to_date: str) -> list[SyncedGithubContributionDay]:
        target_year = int(to_date[:4])
        parsed: list[SyncedGithubContributionDay] = []
        for match in _TOOLTIP_DAY_PATTERN.finditer(html):
            month_number = _MONTHS.get(match.group('month'))
            if month_number is None:
                continue
            day_number = int(match.group('day'))
            count = max(int(match.group('count')), 0)
            contribution_date = date(target_year, month_number, day_number)
            parsed.append(
                SyncedGithubContributionDay(
                    date=contribution_date.isoformat(),
                    count=count,
                    level=self._level_from_count(count),
                )
            )
        parsed.sort(key=lambda item: item.date)
        return parsed

    def _get_json(self, url: str) -> dict[str, Any] | list[Any]:
        text = self._get_text(url, accept='application/vnd.github+json')
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise GithubStatsSyncError(f'GitHub returned invalid JSON for {url}.') from exc

    def _get_text(self, url: str, *, accept: str) -> str:
        headers = {
            'Accept': accept,
            'User-Agent': 'portfolio-api-service',
            'X-GitHub-Api-Version': self.api_version,
        }
        token = self.settings.github_api_token.strip()
        if token and 'api.github.com' in url:
            headers['Authorization'] = f'Bearer {token}'
        req = request.Request(url, headers=headers)
        try:
            with request.urlopen(req, timeout=20) as response:
                return response.read().decode('utf-8')
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore')
            raise GithubStatsSyncError(f'GitHub request failed: {exc.code} {detail or exc.reason}') from exc
        except error.URLError as exc:
            raise GithubStatsSyncError(f'GitHub request failed: {exc.reason}') from exc

    def _to_int_or_none(self, value: Any) -> int | None:
        if value is None:
            return None
        try:
            return max(int(value), 0)
        except (TypeError, ValueError):
            return None

    def _level_from_count(self, count: int) -> int:
        if count <= 0:
            return 0
        if count <= 2:
            return 1
        if count <= 5:
            return 2
        if count <= 10:
            return 3
        return 4
