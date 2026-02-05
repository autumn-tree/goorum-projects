import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
# 통합 국가 대시보드
# -----------------------------
def build_national_dashboard(df):

    # 🔥 2-row dashboard
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        specs=[
            [{"secondary_y": True}],   # 신규 그래프 (dual axis)
            [{"secondary_y": False}]  # 누적 그래프
        ],
        subplot_titles=(
            "국내 신규 확진자 / 사망자 추이",
            "국내 누적 확진자 / 사망자 추이"
        )
    )

    # -------------------------
    # 1. 신규 확진자 / 사망자 (Dual Axis)
    # -------------------------
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["new_cases"],
            name="신규 확진자",
            mode="lines"
        ),
        row=1,
        col=1,
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["new_deaths"],
            name="신규 사망자",
            mode="lines"
        ),
        row=1,
        col=1,
        secondary_y=True
    )

    # -------------------------
    # 2. 누적 확진자 / 사망자
    # -------------------------
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["cum_cases"],
            name="누적 확진자",
            mode="lines"
        ),
        row=2,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["cum_deaths"],
            name="누적 사망자",
            mode="lines"
        ),
        row=2,
        col=1
    )

    # -------------------------
    # Layout
    # -------------------------
    fig.update_layout(
        title="대한민국 코로나19 전국 통합 대시보드",
        template="plotly_dark",
        height=850,
        hovermode="x unified",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            font=dict(family="Arial", size=13)
        ),

        margin=dict(l=60, r=60, t=120, b=60)
    )

    # X axis
    fig.update_xaxes(
        title_text="날짜",
        showgrid=False,
        title_font=dict(family="Arial", size=15),
        tickfont=dict(family="Arial")
    )

    # Y axis (신규 확진자)
    fig.update_yaxes(
        title_text="확진자 수",
        row=1,
        col=1,
        secondary_y=False,
        showgrid=False
    )

    # Y axis (신규 사망자)
    fig.update_yaxes(
        title_text="사망자 수",
        row=1,
        col=1,
        secondary_y=True,
        showgrid=False
    )

    # Y axis (누적)
    fig.update_yaxes(
        title_text="누적 수",
        row=2,
        col=1,
        showgrid=False
    )

    fig.show()


# -----------------------------
# 실행
# -----------------------------
def main():
    df = load_data()
    build_national_dashboard(df)


if __name__ == "__main__":
    main()
