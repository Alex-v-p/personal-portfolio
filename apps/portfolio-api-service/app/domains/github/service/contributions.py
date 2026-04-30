from __future__ import annotations

from datetime import date, timedelta
import json
import re
from typing import Any, Callable
from urllib import error, parse, request

from app.core.config import get_settings
from app.domains.github.service.models import GithubStatsSyncError, SyncedGithubContributionDay

_LEVEL_MAP = {
    'NONE': 0,
    'FIRST_QUARTILE': 1,
    'SECOND_QUARTILE': 2,
    'THIRD_QUARTILE': 3,
    'FOURTH_QUARTILE': 4,
}
_SVG_RECT_PATTERN = re.compile(r'<rect\b(?P<attrs>[^>]*)>', re.IGNORECASE)
_SVG_ATTR_PATTERN = re.compile(r'(?P<name>data-date|data-count|data-level)="(?P<value>[^"]*)"')
_TOOLTIP_DAY_PATTERN = re.compile(
    r'(?P<count>[0-9]+|No) contribution[s]? on (?P<month>[A-Za-z]+) (?P<day>[0-9]{1,2})(?:st|nd|rd|th)'
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
    days: list[SyncedGithubContributionDay] = []
    for rect_match in _SVG_RECT_PATTERN.finditer(html):
        attrs = {match.group('name'): match.group('value') for match in _SVG_ATTR_PATTERN.finditer(rect_match.group('attrs'))}
        raw_date = attrs.get('data-date')
        raw_count = attrs.get('data-count')
        raw_level = attrs.get('data-level')
        if raw_date is None or raw_count is None or raw_level is None:
            continue
        try:
            date.fromisoformat(raw_date)
            count = max(int(raw_count), 0)
            level = max(int(raw_level), 0)
        except ValueError:
            continue
        days.append(SyncedGithubContributionDay(date=raw_date, count=count, level=level))

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


def parse_tooltip_contribution_days(html: str, *, from_date: str, to_date: str) -> list[SyncedGithubContributionDay]:
    window_start = date.fromisoformat(from_date)
    window_end = date.fromisoformat(to_date)
    target_year = window_end.year
    parsed: list[SyncedGithubContributionDay] = []
    for match in _TOOLTIP_DAY_PATTERN.finditer(html):
        month_number = _MONTHS.get(match.group('month'))
        if month_number is None:
            continue

        candidate_year = target_year - 1 if month_number > window_end.month else target_year

        try:
            contribution_date = date(candidate_year, month_number, int(match.group('day')))
        except ValueError:
            continue

        if contribution_date < window_start or contribution_date > window_end:
            continue

        raw_count = match.group('count')
        count = 0 if raw_count == 'No' else max(int(raw_count), 0)
        parsed.append(
            SyncedGithubContributionDay(
                date=contribution_date.isoformat(),
                count=count,
                level=level_from_count(count),
            )
        )

    parsed.sort(key=lambda item: item.date)
    return parsed


def normalize_contribution_day_window(
    days: list[SyncedGithubContributionDay],
    *,
    from_date: str,
    to_date: str,
) -> list[SyncedGithubContributionDay]:
    window_start = date.fromisoformat(from_date)
    window_end = date.fromisoformat(to_date)
    deduped: dict[str, SyncedGithubContributionDay] = {}
    for day in days:
        try:
            contribution_date = date.fromisoformat(day.date)
        except ValueError:
            continue
        if contribution_date < window_start or contribution_date > window_end:
            continue
        deduped[contribution_date.isoformat()] = SyncedGithubContributionDay(
            date=contribution_date.isoformat(),
            count=max(int(day.count), 0),
            level=max(int(day.level), 0),
        )

    normalized: list[SyncedGithubContributionDay] = []
    cursor = window_start
    while cursor <= window_end:
        key = cursor.isoformat()
        normalized.append(
            deduped.get(
                key,
                SyncedGithubContributionDay(
                    date=key,
                    count=0,
                    level=0,
                ),
            )
        )
        cursor += timedelta(days=1)

    return normalized


def _summarize_graphql_errors(errors: Any) -> str:
    if not isinstance(errors, list):
        return str(errors)

    messages: list[str] = []
    for entry in errors:
        if isinstance(entry, dict):
            message = entry.get('message')
            if isinstance(message, str) and message.strip():
                messages.append(message.strip())
        elif isinstance(entry, str) and entry.strip():
            messages.append(entry.strip())

    return '; '.join(messages) if messages else str(errors)


def _format_graphql_http_error(status_code: int, detail: str) -> str:
    normalized_detail = detail.strip()
    if status_code == 401:
        return 'GitHub GraphQL authentication failed. Check that GITHUB_API_TOKEN is valid.'
    if status_code == 403:
        lowered = normalized_detail.lower()
        if 'rate limit' in lowered:
            return 'GitHub GraphQL rate limit was reached. Wait for the reset or use a token with available quota.'
        return f'GitHub GraphQL access was forbidden. Check token scopes, SSO authorization, rate limits, and profile visibility. Detail: {normalized_detail}'
    if status_code == 404:
        return 'GitHub GraphQL endpoint returned 404. Check network access and the configured GitHub API endpoint.'
    return f'GitHub GraphQL request failed with HTTP {status_code}: {normalized_detail}'


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
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (compatible; portfolio-api-service/1.0; +https://github.com)',
                'X-GitHub-Api-Version': '2022-11-28',
            },
            method='POST',
        )
        try:
            with request.urlopen(req, timeout=20) as response:
                payload = json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore')
            raise GithubStatsSyncError(_format_graphql_http_error(exc.code, detail or exc.reason)) from exc
        except error.URLError as exc:
            raise GithubStatsSyncError(f'GitHub GraphQL request failed before a response was received: {exc.reason}') from exc
        except json.JSONDecodeError as exc:
            raise GithubStatsSyncError('GitHub GraphQL returned invalid JSON.') from exc

        errors = payload.get('errors')
        if errors:
            message = _summarize_graphql_errors(errors)
            if 'Could not resolve to a User' in message or 'Could not resolve to a user' in message:
                raise GithubStatsSyncError('GitHub username not found in GraphQL. Check the configured username.')
            raise GithubStatsSyncError(f'GitHub GraphQL returned errors: {message}')

        user_payload = (payload.get('data') or {}).get('user')
        if user_payload is None:
            raise GithubStatsSyncError('GitHub username not found in GraphQL. Check the configured username.')

        calendar = ((user_payload.get('contributionsCollection') or {}).get('contributionCalendar'))
        if not isinstance(calendar, dict):
            raise GithubStatsSyncError('GitHub GraphQL contribution calendar was missing from the response. Check token access and GitHub profile availability.')

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

        normalized_days = normalize_contribution_day_window(contribution_days, from_date=from_date, to_date=to_date)
        return normalized_days, {
            'source': 'graphql',
            'from': from_date,
            'to': to_date,
            'totalContributions': max(int(calendar.get('totalContributions') or 0), 0),
            'days': len(normalized_days),
        }

    def fetch_public(
        self,
        *,
        username: str,
        from_date: str,
        to_date: str,
        svg_fetcher: Callable[[str], str],
        html_fetcher: Callable[[str], str] | None = None,
    ) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
        window_start = date.fromisoformat(from_date)
        window_end = date.fromisoformat(to_date)
        if window_start.year != window_end.year:
            return self._fetch_public_segmented(
                username=username,
                from_date=from_date,
                to_date=to_date,
                svg_fetcher=svg_fetcher,
                html_fetcher=html_fetcher,
            )

        query = parse.urlencode({'from': from_date, 'to': to_date})
        url = f'https://github.com/users/{parse.quote(username)}/contributions?{query}'
        fetch_errors: list[str] = []

        try:
            svg_or_html = svg_fetcher(url)
            days = parse_svg_contribution_days(svg_or_html)
            if days:
                normalized_days = normalize_contribution_day_window(days, from_date=from_date, to_date=to_date)
                return normalized_days, {
                    'source': 'public-profile-svg',
                    'from': from_date,
                    'to': to_date,
                    'totalContributions': sum(day.count for day in normalized_days),
                    'days': len(normalized_days),
                }
        except GithubStatsSyncError as exc:
            fetch_errors.append(str(exc))

        fallback_fetcher = html_fetcher or svg_fetcher
        try:
            html = fallback_fetcher(url)
        except GithubStatsSyncError as exc:
            fetch_errors.append(str(exc))
            error_suffix = f" Details: {' | '.join(fetch_errors)}" if fetch_errors else ''
            raise GithubStatsSyncError(
                'GitHub public contribution scraping failed. Use a valid GITHUB_API_TOKEN for the most reliable full-year contribution calendar.'
                + error_suffix
            ) from exc

        days = parse_tooltip_contribution_days(html, from_date=from_date, to_date=to_date)
        if not days:
            error_suffix = f" Details: {' | '.join(fetch_errors)}" if fetch_errors else ''
            raise GithubStatsSyncError(
                'GitHub contribution graph could not be parsed from the public profile response. The profile may be private, the markup may have changed, or GitHub may have blocked scraping. Configure GITHUB_API_TOKEN to use GraphQL instead.'
                + error_suffix
            )

        if len(days) < 84:
            raise GithubStatsSyncError(
                'GitHub only exposed an incomplete contribution summary during public scraping. Configure GITHUB_API_TOKEN so the CMS refresh can use the GraphQL contribution calendar and import the full daily board.'
            )

        normalized_days = normalize_contribution_day_window(days, from_date=from_date, to_date=to_date)
        return normalized_days, {
            'source': 'public-profile-html',
            'from': from_date,
            'to': to_date,
            'totalContributions': sum(day.count for day in normalized_days),
            'days': len(normalized_days),
        }

    def _fetch_public_segmented(
        self,
        *,
        username: str,
        from_date: str,
        to_date: str,
        svg_fetcher: Callable[[str], str],
        html_fetcher: Callable[[str], str] | None = None,
    ) -> tuple[list[SyncedGithubContributionDay], dict[str, Any]]:
        window_start = date.fromisoformat(from_date)
        window_end = date.fromisoformat(to_date)
        current = window_start
        merged_days: list[SyncedGithubContributionDay] = []
        segment_meta: list[dict[str, Any]] = []

        while current <= window_end:
            segment_end = min(date(current.year, 12, 31), window_end)
            days, meta = self.fetch_public(
                username=username,
                from_date=current.isoformat(),
                to_date=segment_end.isoformat(),
                svg_fetcher=svg_fetcher,
                html_fetcher=html_fetcher,
            )
            merged_days.extend(days)
            segment_meta.append(meta)
            current = segment_end + timedelta(days=1)

        normalized_days = normalize_contribution_day_window(merged_days, from_date=from_date, to_date=to_date)
        return normalized_days, {
            'source': 'public-profile-segmented',
            'from': from_date,
            'to': to_date,
            'totalContributions': sum(day.count for day in normalized_days),
            'days': len(normalized_days),
            'segments': len(segment_meta),
            'segmentSources': [meta.get('source') for meta in segment_meta],
        }

