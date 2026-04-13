from __future__ import annotations

from datetime import date
import json
import re
from typing import Any, Callable
from urllib import parse, request, error

from app.core.config import get_settings
from app.services.github_stats.models import GithubStatsSyncError, SyncedGithubContributionDay

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


def parse_svg_contribution_days(html: str) -> list[SyncedGithubContributionDay]:
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


def level_from_count(count: int) -> int:
    if count <= 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 10:
        return 3
    return 4


def parse_tooltip_contribution_days(html: str, *, to_date: str) -> list[SyncedGithubContributionDay]:
    target_year = int(to_date[:4])
    parsed: list[SyncedGithubContributionDay] = []
    for match in _TOOLTIP_DAY_PATTERN.finditer(html):
        month_number = _MONTHS.get(match.group('month'))
        if month_number is None:
            continue
        contribution_date = date(target_year, month_number, int(match.group('day')))
        count = max(int(match.group('count')), 0)
        parsed.append(
            SyncedGithubContributionDay(
                date=contribution_date.isoformat(),
                count=count,
                level=level_from_count(count),
            )
        )
    parsed.sort(key=lambda item: item.date)
    return parsed


class GithubContributionSyncClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def fetch_graphql(self, *, username: str, from_date: str, to_date: str) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
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
        body = json.dumps(
            {
                'query': query,
                'variables': {
                    'login': username,
                    'from': f'{from_date}T00:00:00Z',
                    'to': f'{to_date}T23:59:59Z',
                },
            }
        ).encode('utf-8')
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

    def fetch_public(self, *, username: str, from_date: str, to_date: str, html_fetcher: Callable[[str], str]) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
        query = parse.urlencode({'from': from_date, 'to': to_date})
        html = html_fetcher(f'https://github.com/users/{parse.quote(username)}/contributions?{query}')
        days = parse_svg_contribution_days(html)
        if not days:
            days = parse_tooltip_contribution_days(html, to_date=to_date)
        if not days:
            raise GithubStatsSyncError('GitHub contribution graph could not be parsed from the public profile response.')
        return days, {
            'source': 'public-profile',
            'from': from_date,
            'to': to_date,
            'totalContributions': sum(day.count for day in days),
        }
