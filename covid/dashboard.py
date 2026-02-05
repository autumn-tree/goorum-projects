import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.templates.default = "plotly_dark"


# load data
def load_data():
    base = Path(__file__).resolve().parent / "data"

    national = pd.read_csv(base / "a_national_trend_daily.csv")
    sigungu_cases = pd.read_csv(base / "b_sigungu_monthly_cases.csv")
    sigungu_deaths = pd.read_csv(base / "b_sigungu_monthly_deaths.csv")
    region_latest = pd.read_csv(base / "b_region_latest.csv")
    region_daily = pd.read_csv(base / "b_region_daily_timeseries.csv")
    vax = pd.read_csv(base / "c_vax_vs_fatality_proxy.csv")

    # datetime conversion
    national["date"] = pd.to_datetime(national["date"])
    sigungu_cases["date"] = pd.to_datetime(sigungu_cases["date"])
    sigungu_deaths["date"] = pd.to_datetime(sigungu_deaths["date"])
    region_daily["date"] = pd.to_datetime(region_daily["date"])
    vax["date"] = pd.to_datetime(vax["date"])

    return national, sigungu_cases, sigungu_deaths, region_latest, region_daily, vax


# build dashboard
def build_dashboard(national, sigungu_cases, sigungu_deaths, region_latest, region_daily, vax):

    fig = make_subplots(
        rows=3,
        cols=2,
        subplot_titles=[
            "국내 일일 확진자 및 사망자 추이",
            "국내 누적 확진자 및 사망자 추이",
            "지역별 누적 확진자 현황",
            "백신 접종률 vs 치명률",
            "주요 지역 일일 확진자 추이",
            "주요 시군구 월별 확진자 추이"
        ],
        vertical_spacing=0.15,     # 그래프 위아래 여백 
        horizontal_spacing=0.08    # 좌우 여백
    )

    # 1️⃣ 일일 확진자/사망자
    fig.add_trace(
        go.Scatter(
            x=national["date"],
            y=national["new_cases"],
            name="일일 확진자",
            mode="lines"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=national["date"],
            y=national["new_deaths"],
            name="일일 사망자",
            mode="lines"
        ),
        row=1, col=1
    )

    # 2️⃣ 누적 추이
    fig.add_trace(
        go.Scatter(
            x=national["date"],
            y=national["cum_cases"],
            name="누적 확진자",
            mode="lines"
        ),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(
            x=national["date"],
            y=national["cum_deaths"],
            name="누적 사망자",
            mode="lines"
        ),
        row=1, col=2
    )

    # 3️⃣ 지역별 누적 확진자
    fig.add_trace(
        go.Bar(
            x=region_latest["region"],
            y=region_latest["cum_cases"],
            name="지역별 누적 확진자"
        ),
        row=2, col=1
    )

    # 4️⃣ 백신 vs 치명률
    fig.add_trace(
        go.Scatter(
            x=vax["vax2_rate"],
            y=vax["fatality_rate_7d"],
            mode="markers",
            name="2차 접종률 vs 치명률"
        ),
        row=2, col=2
    )

    # 5️⃣ 지역별 일일 확진자 (상위 3개 지역)
    top_regions = region_daily["region"].value_counts().head(3).index

    for r in top_regions:
        temp = region_daily[region_daily["region"] == r]
        fig.add_trace(
            go.Scatter(
                x=temp["date"],
                y=temp["new_cases"],
                mode="lines",
                name=f"{r} 일일확진"
            ),
            row=3, col=1
        )

    # 6️⃣ 시군구 월별 확진자 (상위 5개)
    top_sigungu = (
        sigungu_cases.groupby("sigungu")["monthly_cases"]
        .sum()
        .nlargest(5)
        .index
    )

    for s in top_sigungu:
        temp = sigungu_cases[sigungu_cases["sigungu"] == s]
        fig.add_trace(
            go.Scatter(
                x=temp["date"],
                y=temp["monthly_cases"],
                mode="lines",
                name=f"{s} 월별확진"
            ),
            row=3, col=2
        )

    # 레이아웃
    fig.update_layout(
    height=1000,

    margin=dict(
        l=60,
        r=60,
        t=100,   
        b=60
    ),

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.15,       
        xanchor="center",
        x=0.5,

        itemwidth=40,
        tracegroupgap=15,
        font=dict(size=12)
    )
)

    fig.show()


# main
def main():
    national, sigungu_cases, sigungu_deaths, region_latest, region_daily, vax = load_data()
    build_dashboard(national, sigungu_cases, sigungu_deaths, region_latest, region_daily, vax)


if __name__ == "__main__":
    main()
