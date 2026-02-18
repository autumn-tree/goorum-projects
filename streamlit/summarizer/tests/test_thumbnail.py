from __future__ import annotations

import pytest

from src.thumbnail import (
    ThumbnailCandidate,
    ThumbnailExtractionError,
    build_thumbnail_candidates,
    extract_thumbnail_from_url,
    extract_video_id_from_url,
    resolve_best_thumbnail,
)


def test_extract_video_id_from_watch_url() -> None:
    video_id = extract_video_id_from_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert video_id == "dQw4w9WgXcQ"


def test_extract_video_id_from_youtu_be_url() -> None:
    video_id = extract_video_id_from_url("https://youtu.be/dQw4w9WgXcQ?t=30")
    assert video_id == "dQw4w9WgXcQ"


def test_extract_video_id_from_shorts_url() -> None:
    video_id = extract_video_id_from_url("https://www.youtube.com/shorts/dQw4w9WgXcQ")
    assert video_id == "dQw4w9WgXcQ"


def test_extract_video_id_rejects_non_youtube_domains() -> None:
    with pytest.raises(ThumbnailExtractionError):
        extract_video_id_from_url("https://vimeo.com/123456")


def test_extract_video_id_rejects_invalid_or_missing_ids() -> None:
    with pytest.raises(ThumbnailExtractionError):
        extract_video_id_from_url("https://www.youtube.com/watch?v=short")
    with pytest.raises(ThumbnailExtractionError):
        extract_video_id_from_url("https://www.youtube.com/watch")


def test_build_thumbnail_candidates_has_expected_priority_order() -> None:
    candidates = build_thumbnail_candidates("dQw4w9WgXcQ")
    assert [candidate.quality for candidate in candidates] == [
        "maxresdefault",
        "hqdefault",
        "mqdefault",
        "default",
    ]


def test_resolve_best_thumbnail_uses_fallback_order() -> None:
    checks: dict[str, bool] = {
        "maxresdefault": False,
        "hqdefault": False,
        "mqdefault": True,
        "default": True,
    }

    def checker(candidate: ThumbnailCandidate) -> bool:
        return checks[candidate.quality]

    selected = resolve_best_thumbnail("dQw4w9WgXcQ", checker=checker)
    assert selected.quality == "mqdefault"
    assert selected.url.endswith("/mqdefault.jpg")


def test_resolve_best_thumbnail_raises_when_no_thumbnail_available() -> None:
    def checker(_: ThumbnailCandidate) -> bool:
        return False

    with pytest.raises(ThumbnailExtractionError):
        resolve_best_thumbnail("dQw4w9WgXcQ", checker=checker)


def test_extract_thumbnail_from_url_combines_parse_and_resolve() -> None:
    def checker(candidate: ThumbnailCandidate) -> bool:
        return candidate.quality == "hqdefault"

    video_id, selected = extract_thumbnail_from_url(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        checker=checker,
    )
    assert video_id == "dQw4w9WgXcQ"
    assert selected.quality == "hqdefault"
