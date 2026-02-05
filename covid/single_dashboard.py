import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.io as pio

# template
pio.templates.default = "plotly_dark"


# -----------------------------
# 데이터 로드
# -----------------------------
def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "a_national_trend_daily.csv"

    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])

    return df


# -----------------------------
# 단일 그래프 대시보드
# -----------------------------
def build_single_dashboard(df):

    fig = go.Figure()

    # 일일 확진자
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["new_cases"],
            mode="lines",
            name="● 일일 확진자"
        )
    )

    # 일일 사망자
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["new_deaths"],
            mode="lines",
            name="● 일일 사망자"
        )
    )

    # 누적 확진자
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["cum_cases"],
            mode="lines",
            name="● 누적 확진자"
        )
    )

    # 누적 사망자
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["cum_deaths"],
            mode="lines",
            name="● 누적 사망자"
        )
    )

    # 레이아웃
    fig.update_layout(
        title="대한민국 코로나19 전국 확진자 및 사망자 통합 추이",
        height=650,

        margin=dict(l=60, r=60, t=120, b=60),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        ),

        xaxis_title="날짜",
        yaxis_title="건수"
    )

    fig.show()


# -----------------------------
# 실행
# -----------------------------
def main():
    df = load_data()
    build_single_dashboard(df)


if __name__ == "__main__":
    main()
