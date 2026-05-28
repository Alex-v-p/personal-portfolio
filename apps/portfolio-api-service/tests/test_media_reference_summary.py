from app.services.media.models import MediaReferenceSummary


def test_media_reference_summary_tracks_totals_and_reference_flag() -> None:
    summary = MediaReferenceSummary(
        profile_avatar_count=1,
        project_cover_count=2,
        blog_cover_count=1,
    )

    assert summary.total_references == 4
    assert summary.is_referenced is True


def test_media_reference_summary_defaults_to_unused() -> None:
    summary = MediaReferenceSummary()

    assert summary.total_references == 0
    assert summary.is_referenced is False
