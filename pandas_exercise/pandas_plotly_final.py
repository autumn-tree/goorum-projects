import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go
import numpy as np
import plotly.graph_objects as go

# 데이터 로드
def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "netflix_titles.csv"
    df = pd.read_csv(data_path)

    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    df = df.dropna(subset=["release_year"])

    return df


def basic_chart(df):
    yearly = df.groupby("release_year").size().reset_index(name="count")

    fig = px.line(
        yearly,
        x="release_year",
        y="count",
        title="넷플릭스 연도별 콘텐츠 수"
    )

    fig.show()


def modebar_chart(df):
    yearly = df.groupby("release_year").size()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=yearly.index,
            y=yearly.values,
            mode="lines+markers",
            name="콘텐츠 수"
        )
    )

    fig.update_layout(
        title="모드바 인터랙션 차트",
        dragmode="zoom"   # 기본 인터랙션
    )

    fig.show(config={
        "displayModeBar": True,
        "modeBarButtonsToAdd": [
            "drawline",
            "drawrect",
            "eraseshape"
        ]
    })


def slider_chart(df):
    yearly = df.groupby("release_year").size()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=yearly.index,
            y=yearly.values,
            name="콘텐츠 수"
        )
    )

    fig.update_layout(
        title="연도 슬라이더 인터랙티브 차트",
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="linear"
        )
    )

    fig.show()


def scientific_chart(df):
    yearly = df.groupby("release_year").size().reset_index(name="count")

    x = yearly["release_year"]
    y = yearly["count"]

    # 회귀선
    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name="데이터"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=trend(x),
            mode="lines",
            name="Trend Line"
        )
    )

    fig.update_layout(
        title="Scientific Analysis Chart (콘텐츠 증가 추세)"
    )

    fig.show()

def main():
    df = load_data()
    basic_chart(df)
    modebar_chart(df)
    slider_chart(df)
    scientific_chart(df)

if __name__ == "__main__":
    main()
