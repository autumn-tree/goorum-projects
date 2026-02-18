from __future__ import annotations

from datetime import UTC, datetime

import streamlit as st

from src.charts import (
    build_category_bar_chart,
    build_region_heatmap,
    build_trend_line_chart,
)
from src.data_loader import load_kosis_data
from src.eda import (
    build_category_summary,
    build_grouped_stats,
    build_missing_value_profile,
    build_monthly_trend,
    build_region_category_pivot,
    filter_kosis_data,
    get_summary_metrics,
)
from src.preprocessing import get_preprocess_refresh_timestamp, preprocess_kosis_data
from src.session_manager import (
    append_history,
    get_state,
    init_session_state,
    reset_filters,
    reset_session,
    set_state,
)
from src.thumbnail import (
    ThumbnailExtractionError,
    extract_thumbnail_from_url,
    fetch_thumbnail_bytes,
)


def render_sidebar() -> None:
    """Render navigation and session controls."""
    pages = ["Dashboard", "Thumbnail Extractor", "Debug"]
    current_page = get_state(st.session_state, "page", "Dashboard")
    selected_page = st.sidebar.radio(
        "Navigate",
        pages,
        index=pages.index(current_page) if current_page in pages else 0,
    )

    if selected_page != current_page:
        set_state(st.session_state, "page", selected_page)
        append_history(st.session_state, "navigate", {"page": selected_page})

    st.sidebar.divider()
    st.sidebar.subheader("Session Controls")

    if st.sidebar.button("Reset Filters"):
        reset_filters(st.session_state)
        append_history(st.session_state, "reset_filters")
        st.sidebar.success("Filters reset.")

    if st.sidebar.button("Reset Session"):
        reset_session(st.session_state)
        append_history(st.session_state, "reset_session")
        st.sidebar.success("Session reset.")

    st.sidebar.divider()
    st.sidebar.subheader("Cache Controls")

    if st.sidebar.button("Clear Data Cache"):
        st.cache_data.clear()
        set_state(
            st.session_state,
            "cache_version",
            int(get_state(st.session_state, "cache_version", 1)) + 1,
        )
        set_state(
            st.session_state,
            "last_data_cache_cleared_at",
            datetime.now(UTC).isoformat(),
        )
        append_history(st.session_state, "clear_data_cache")
        st.sidebar.success("Data cache cleared.")

    if st.sidebar.button("Reinitialize Resources"):
        st.cache_resource.clear()
        set_state(
            st.session_state,
            "cache_version",
            int(get_state(st.session_state, "cache_version", 1)) + 1,
        )
        set_state(
            st.session_state,
            "last_resource_cache_cleared_at",
            datetime.now(UTC).isoformat(),
        )
        append_history(st.session_state, "clear_resource_cache")
        st.sidebar.success("Resource cache reinitialized.")


def render_dashboard_page() -> None:
    st.header("KOSIS Dashboard")
    st.caption("Phase 3: EDA and Plotly visualization are enabled.")

    api_url = st.text_input(
        "KOSIS API URL (Optional)",
        placeholder="https://example.com/kosis-endpoint",
        help="If empty or failing, the app loads local sample data.",
    ).strip()

    raw_df, source, data_refresh_ts = load_kosis_data(
        api_url=api_url or None,
        local_path="data/raw/kosis_sample.csv",
    )
    processed_df = preprocess_kosis_data(raw_df)
    preprocess_refresh_ts = get_preprocess_refresh_timestamp(raw_df)
    if processed_df.empty:
        st.warning("No valid rows after preprocessing. Check source data.")
        return

    set_state(st.session_state, "selected_dataset", "kosis")
    set_state(st.session_state, "last_data_source", source)
    set_state(st.session_state, "last_data_refresh_ts", data_refresh_ts)
    set_state(st.session_state, "last_preprocess_refresh_ts", preprocess_refresh_ts)

    source_label = {
        "api": "API",
        "local": "Local CSV",
        "local_fallback": "Local CSV (API fallback)",
    }.get(source, source)
    st.info(f"Data source: {source_label}")

    available_regions = sorted(processed_df["region"].dropna().unique().tolist())
    available_categories = sorted(processed_df["category"].dropna().unique().tolist())
    year_min = int(processed_df["year"].min())
    year_max = int(processed_df["year"].max())

    saved_filters = get_state(st.session_state, "filters", {})
    default_regions = [
        region for region in saved_filters.get("regions", []) if region in available_regions
    ]
    default_categories = [
        category
        for category in saved_filters.get("categories", [])
        if category in available_categories
    ]
    default_year_range = saved_filters.get("date_range")
    if (
        not isinstance(default_year_range, tuple)
        or len(default_year_range) != 2
        or not all(isinstance(value, int) for value in default_year_range)
    ):
        default_year_range = (year_min, year_max)

    f_col1, f_col2, f_col3 = st.columns(3)
    selected_regions = f_col1.multiselect(
        "Regions",
        options=available_regions,
        default=default_regions,
    )
    selected_categories = f_col2.multiselect(
        "Categories",
        options=available_categories,
        default=default_categories,
    )
    selected_year_range = f_col3.slider(
        "Year Range",
        min_value=year_min,
        max_value=year_max,
        value=default_year_range,
    )

    set_state(
        st.session_state,
        "filters",
        {
            "regions": selected_regions,
            "categories": selected_categories,
            "date_range": selected_year_range,
        },
    )

    filtered_df = filter_kosis_data(
        processed_df,
        regions=selected_regions,
        categories=selected_categories,
        year_range=selected_year_range,
    )
    if filtered_df.empty:
        st.warning("No rows match the selected filters.")
        return

    metrics = get_summary_metrics(filtered_df)
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    m_col1.metric("Raw Rows", len(raw_df))
    m_col2.metric("Filtered Rows", metrics["rows"])
    m_col3.metric("Regions", metrics["regions"])
    m_col4.metric("Total Value", f"{metrics['total_value']:,.2f}")
    m_col5.metric("Average Value", f"{metrics['avg_value']:,.2f}")

    trend_df = build_monthly_trend(filtered_df)
    category_df = build_category_summary(filtered_df)
    heatmap_df = build_region_category_pivot(filtered_df)

    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.plotly_chart(build_trend_line_chart(trend_df), use_container_width=True)
    with c_col2:
        st.plotly_chart(build_category_bar_chart(category_df), use_container_width=True)

    if not heatmap_df.empty:
        st.plotly_chart(build_region_heatmap(heatmap_df), use_container_width=True)

    with st.expander("Raw Data Preview", expanded=False):
        st.dataframe(raw_df.head(100), use_container_width=True)

    with st.expander("EDA Summary", expanded=False):
        grouped_stats = build_grouped_stats(filtered_df, ["region", "category"])
        missing_profile = build_missing_value_profile(raw_df)
        st.write("Grouped Statistics (Region x Category)")
        st.dataframe(grouped_stats, use_container_width=True)
        st.write("Missing Value Profile (Raw Data)")
        st.dataframe(missing_profile, use_container_width=True)

    with st.expander("Processed Data Preview", expanded=True):
        styled = filtered_df.head(200).style.set_properties(
            subset=["month"],
            **{"text-align": "right"},
        )
        st.dataframe(styled, use_container_width=True)


def render_thumbnail_page() -> None:
    st.header("YouTube Thumbnail Extractor")
    st.caption("Supports YouTube video and shorts URLs only.")

    def clear_thumbnail_result_state() -> None:
        set_state(st.session_state, "last_thumbnail_video_id", None)
        set_state(st.session_state, "last_thumbnail_quality", None)
        set_state(st.session_state, "last_thumbnail_url", None)

    youtube_url = st.text_input(
        "YouTube URL",
        placeholder=(
            "https://www.youtube.com/watch?v=... | https://youtu.be/... | "
            "https://www.youtube.com/shorts/..."
        ),
    ).strip()

    if st.button("Extract Thumbnail", type="primary"):
        if not youtube_url:
            clear_thumbnail_result_state()
            st.error("Please enter a YouTube video or shorts URL.")
            return

        try:
            video_id, candidate = extract_thumbnail_from_url(youtube_url)
            set_state(st.session_state, "last_thumbnail_video_id", video_id)
            set_state(st.session_state, "last_thumbnail_quality", candidate.quality)
            set_state(st.session_state, "last_thumbnail_url", candidate.url)
            append_history(
                st.session_state,
                "extract_thumbnail",
                {"video_id": video_id, "quality": candidate.quality},
            )
        except ThumbnailExtractionError as error:
            clear_thumbnail_result_state()
            st.error(str(error))
            return
        except Exception:
            clear_thumbnail_result_state()
            st.error("Unable to extract thumbnail due to a network or availability error.")
            return

    thumbnail_url = get_state(st.session_state, "last_thumbnail_url")
    if thumbnail_url:
        st.success(
            "Thumbnail resolved: "
            f"{get_state(st.session_state, 'last_thumbnail_quality', 'unknown')}"
        )
        st.image(thumbnail_url, caption=f"Video ID: {get_state(st.session_state, 'last_thumbnail_video_id', '')}")

        st.link_button("Open Thumbnail URL", thumbnail_url)
        try:
            image_bytes = fetch_thumbnail_bytes(thumbnail_url)
            st.download_button(
                "Download Thumbnail",
                data=image_bytes,
                file_name=f"{get_state(st.session_state, 'last_thumbnail_video_id', 'thumbnail')}.jpg",
                mime="image/jpeg",
            )
        except Exception:
            st.warning("Thumbnail preview is available, but download fetch failed.")


def render_debug_page() -> None:
    st.header("Debug")
    st.subheader("Cache Behavior")
    show_cache_diag = st.toggle("Show cache diagnostics", value=False)
    if show_cache_diag:
        cache_info = {
            "cache_version": get_state(st.session_state, "cache_version", 1),
            "last_data_refresh_ts": get_state(st.session_state, "last_data_refresh_ts"),
            "last_preprocess_refresh_ts": get_state(
                st.session_state, "last_preprocess_refresh_ts"
            ),
            "last_data_cache_cleared_at": get_state(
                st.session_state, "last_data_cache_cleared_at"
            ),
            "last_resource_cache_cleared_at": get_state(
                st.session_state, "last_resource_cache_cleared_at"
            ),
        }
        st.json(cache_info)
        st.caption(
            "Tip: cache refresh timestamps remain stable across reruns and change after cache clear."
        )
    else:
        st.caption("Cache diagnostics are hidden. Enable the toggle to inspect details.")

    st.subheader("Session State")
    show_session_diag = st.toggle("Show session state diagnostics", value=False)
    if show_session_diag:
        st.write("Current session state")
        st.json(dict(st.session_state))
    else:
        st.caption("Session state diagnostics are hidden. Enable the toggle to inspect details.")


def main() -> None:
    st.set_page_config(page_title="KOSIS + Thumbnail App", layout="wide")
    st.title("Streamlit Multi-Feature App")

    init_session_state(st.session_state)
    render_sidebar()

    page = get_state(st.session_state, "page", "Dashboard")
    if page == "Dashboard":
        render_dashboard_page()
    elif page == "Thumbnail Extractor":
        render_thumbnail_page()
    else:
        render_debug_page()


if __name__ == "__main__":
    main()
