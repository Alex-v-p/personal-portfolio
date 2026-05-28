from app.domains.github.service.contributions import GithubContributionSyncClient
from app.services.github_stats.contributions import (
    level_from_count,
    normalize_contribution_day_window,
    parse_svg_contribution_days,
    parse_tooltip_contribution_days,
)


def test_parse_svg_contribution_days_sorts_by_date() -> None:
    html = (
        '<rect data-date="2026-04-03" data-count="4" data-level="2"></rect>'
        '<rect data-date="2026-04-01" data-count="0" data-level="0"></rect>'
        '<rect data-date="2026-04-02" data-count="9" data-level="3"></rect>'
    )

    days = parse_svg_contribution_days(html)

    assert [day.date for day in days] == ['2026-04-01', '2026-04-02', '2026-04-03']
    assert [day.count for day in days] == [0, 9, 4]
    assert [day.level for day in days] == [0, 3, 2]


def test_parse_svg_contribution_days_accepts_reordered_attributes() -> None:
    html = (
        '<rect data-level="3" class="ContributionCalendar-day" data-date="2026-04-02" data-count="7"></rect>'
        '<rect data-count="2" data-level="1" data-date="2026-04-01"></rect>'
    )

    days = parse_svg_contribution_days(html)

    assert [day.date for day in days] == ['2026-04-01', '2026-04-02']
    assert [day.count for day in days] == [2, 7]
    assert [day.level for day in days] == [1, 3]


def test_parse_tooltip_contribution_days_uses_target_year_and_level_mapping() -> None:
    html = '1 contribution on January 3rd 12 contributions on February 4th'

    days = parse_tooltip_contribution_days(html, from_date='2026-01-01', to_date='2026-12-31')

    assert [day.date for day in days] == ['2026-01-03', '2026-02-04']
    assert [day.level for day in days] == [1, 4]


def test_parse_tooltip_contribution_days_rolls_months_before_window_end_back_a_year() -> None:
    html = '2 contributions on September 2nd 6 contributions on January 9th 0 contributions on April 1st'

    days = parse_tooltip_contribution_days(html, from_date='2025-04-16', to_date='2026-04-15')

    assert [day.date for day in days] == ['2025-09-02', '2026-01-09', '2026-04-01']
    assert [day.level for day in days] == [1, 3, 0]


def test_normalize_contribution_day_window_fills_missing_dates_with_zeros() -> None:
    normalized = normalize_contribution_day_window(
        parse_svg_contribution_days(
            '<rect data-date="2026-04-02" data-count="9" data-level="3"></rect>'
            '<rect data-date="2026-04-04" data-count="1" data-level="1"></rect>'
        ),
        from_date='2026-04-01',
        to_date='2026-04-04',
    )

    assert [day.date for day in normalized] == ['2026-04-01', '2026-04-02', '2026-04-03', '2026-04-04']
    assert [day.count for day in normalized] == [0, 9, 0, 1]


def test_fetch_public_prefers_svg_calendar_and_returns_full_daily_window() -> None:
    client = GithubContributionSyncClient()

    days, meta = client.fetch_public(
        username='Alex-v-p',
        from_date='2026-04-01',
        to_date='2026-04-04',
        svg_fetcher=lambda _url: (
            '<svg>'
            '<rect data-date="2026-04-02" data-count="9" data-level="3"></rect>'
            '<rect data-date="2026-04-04" data-count="1" data-level="1"></rect>'
            '</svg>'
        ),
        html_fetcher=lambda _url: '',
    )

    assert [day.date for day in days] == ['2026-04-01', '2026-04-02', '2026-04-03', '2026-04-04']
    assert [day.count for day in days] == [0, 9, 0, 1]
    assert meta['source'] == 'public-profile-svg'


def test_fetch_public_splits_cross_year_windows_into_calendar_year_requests() -> None:
    client = GithubContributionSyncClient()
    requested_urls: list[str] = []

    def svg_fetcher(url: str) -> str:
        requested_urls.append(url)
        if 'from=2025-12-30' in url and 'to=2025-12-31' in url:
            return (
                '<svg>'
                '<rect data-date="2025-12-31" data-count="2" data-level="1"></rect>'
                '</svg>'
            )
        if 'from=2026-01-01' in url and 'to=2026-01-02' in url:
            return (
                '<svg>'
                '<rect data-date="2026-01-02" data-count="5" data-level="2"></rect>'
                '</svg>'
            )
        return '<svg></svg>'

    days, meta = client.fetch_public(
        username='Alex-v-p',
        from_date='2025-12-30',
        to_date='2026-01-02',
        svg_fetcher=svg_fetcher,
        html_fetcher=lambda _url: '',
    )

    assert len(requested_urls) == 2
    assert [day.date for day in days] == ['2025-12-30', '2025-12-31', '2026-01-01', '2026-01-02']
    assert [day.count for day in days] == [0, 2, 0, 5]
    assert meta['source'] == 'public-profile-segmented'
    assert meta['segments'] == 2


def test_fetch_public_rejects_weekly_only_html_fallback() -> None:
    client = GithubContributionSyncClient()

    try:
        client.fetch_public(
            username='Alex-v-p',
            from_date='2026-01-01',
            to_date='2026-04-15',
            svg_fetcher=lambda _url: '<html></html>',
            html_fetcher=lambda _url: 'No contributions on January 5th. 9 contributions on April 12th.',
        )
    except Exception as exc:  # noqa: BLE001
        assert 'GITHUB_API_TOKEN' in str(exc)
    else:
        raise AssertionError('Expected incomplete weekly HTML fallback to be rejected.')


def test_level_from_count_matches_expected_buckets() -> None:
    assert [level_from_count(value) for value in [0, 1, 3, 7, 11]] == [0, 1, 2, 3, 4]
