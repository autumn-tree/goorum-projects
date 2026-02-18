from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Figure


def build_trend_line_chart(trend_df: pd.DataFrame) -> Figure:
    """Create a time-series line chart from monthly trend data."""
    fig = px.line(
        trend_df,
        x="date",
        y="total_value",
        title="Monthly Trend",
        markers=True,
    )
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    return fig


def build_category_bar_chart(category_df: pd.DataFrame) -> Figure:
    """Create a category totals bar chart."""
    fig = px.bar(
        category_df,
        x="category",
        y="total_value",
        title="Category Comparison",
        text="total_value",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    return fig


def build_region_heatmap(pivot_df: pd.DataFrame) -> Figure:
    """Create a heatmap for region-category aggregate values."""
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns.tolist(),
            y=pivot_df.index.tolist(),
            colorscale="Blues",
            colorbar={"title": "Value"},
        )
    )
    fig.update_layout(
        title="Region-Category Heatmap",
        xaxis_title="Category",
        yaxis_title="Region",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    return fig
