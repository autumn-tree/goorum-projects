import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 데이터 로드
def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "netflix_titles.csv"
    df = pd.read_csv(data_path)

    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    df = df.dropna(subset=["release_year"])

    return df


# 드롭다운 인터랙티브 그래프
def dropdown_chart(df):
    movie_df = df[df["type"] == "Movie"].groupby("release_year").size()
    tv_df = df[df["type"] == "TV Show"].groupby("release_year").size()

    fig = go.Figure()

    fig.add_trace(go.Bar(x=movie_df.index, y=movie_df.values, name="Movie", visible=True))
    fig.add_trace(go.Bar(x=tv_df.index, y=tv_df.values, name="TV Show", visible=False))

    fig.update_layout(
        title="넷플릭스 콘텐츠 연도별 수 (드롭다운)",
        updatemenus=[
            dict(
                buttons=[
                    dict(label="Movie",
                         method="update",
                         args=[{"visible": [True, False]}]),
                    dict(label="TV Show",
                         method="update",
                         args=[{"visible": [False, True]}]),
                    dict(label="전체",
                         method="update",
                         args=[{"visible": [True, True]}]),
                ]
            )
        ]
    )

    fig.show()


# 버튼 인터랙티브 그래프
def button_chart(df):
    yearly = df.groupby("release_year").size()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=yearly.index, y=yearly.values, mode="lines", name="전체 콘텐츠"))

    fig.update_layout(
        title="넷플릭스 콘텐츠 증가 추이",
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(label="전체",
                         method="relayout",
                         args=[{"xaxis.range": [yearly.index.min(), yearly.index.max()]}]),
                    dict(label="2000년 이후",
                         method="relayout",
                         args=[{"xaxis.range": [2000, yearly.index.max()]}]),
                    dict(label="2015년 이후",
                         method="relayout",
                         args=[{"xaxis.range": [2015, yearly.index.max()]}]),
                ]
            )
        ]
    )

    fig.show()


# Statistics Chart(등급 분포 + 타입 비율)
def statistics_chart(df):
    rating_counts = df["rating"].value_counts().head(10)
    type_counts = df["type"].value_counts()

    fig = make_subplots(rows=1, cols=2, subplot_titles=("등급 분포", "콘텐츠 타입 비율"),
                        specs=[[{"type": "bar"}, {"type": "pie"}]])

    fig.add_trace(
        go.Bar(x=rating_counts.index, y=rating_counts.values, name="Rating"),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(labels=type_counts.index, values=type_counts.values, name="Type"),
        row=1, col=2
    )

    fig.update_layout(title="넷플릭스 통계 차트")

    fig.show()


def main():
    df = load_data()

    dropdown_chart(df)
    button_chart(df)
    statistics_chart(df)


if __name__ == "__main__":
    main()