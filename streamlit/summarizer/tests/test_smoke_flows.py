from __future__ import annotations

from src.data_loader import load_kosis_data
from src.eda import (
    build_category_summary,
    build_monthly_trend,
    build_region_category_pivot,
    filter_kosis_data,
    get_summary_metrics,
)
from src.preprocessing import preprocess_kosis_data
from src.thumbnail import ThumbnailCandidate, extract_thumbnail_from_url


def test_dashboard_pipeline_smoke() -> None:
    raw_df, source, refresh_ts = load_kosis_data(
        api_url=None,
        local_path="data/raw/kosis_sample.csv",
    )
    assert source == "local"
    assert isinstance(refresh_ts, str) and refresh_ts

    processed_df = preprocess_kosis_data(raw_df)
    filtered_df = filter_kosis_data(
        processed_df,
        regions=["Seoul"],
        categories=["Population"],
        year_range=(2023, 2024),
    )

    metrics = get_summary_metrics(filtered_df)
    trend_df = build_monthly_trend(filtered_df)
    category_df = build_category_summary(filtered_df)
    heatmap_df = build_region_category_pivot(filtered_df)

    assert metrics["rows"] > 0
    assert len(trend_df) > 0
    assert len(category_df) > 0
    assert not heatmap_df.empty


def test_thumbnail_pipeline_smoke_without_network() -> None:
    def checker(candidate: ThumbnailCandidate) -> bool:
        return candidate.quality == "hqdefault"

    video_id, candidate = extract_thumbnail_from_url(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        checker=checker,
    )

    assert video_id == "dQw4w9WgXcQ"
    assert candidate.quality == "hqdefault"
    assert candidate.url.endswith("/hqdefault.jpg")
