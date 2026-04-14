from app.services.github_stats.contributions import level_from_count, parse_svg_contribution_days, parse_tooltip_contribution_days


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


def test_parse_tooltip_contribution_days_uses_target_year_and_level_mapping() -> None:
    html = '1 contribution on January 3rd 12 contributions on February 4th'

    days = parse_tooltip_contribution_days(html, to_date='2026-12-31')

    assert [day.date for day in days] == ['2026-01-03', '2026-02-04']
    assert [day.level for day in days] == [1, 4]


def test_level_from_count_matches_expected_buckets() -> None:
    assert [level_from_count(value) for value in [0, 1, 3, 7, 11]] == [0, 1, 2, 3, 4]
