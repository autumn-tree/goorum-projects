import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# load
def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "netflix_titles.csv"
    return pd.read_csv(data_path)


# overlay
def plot_overlay(df):
    # Prepare data
    movies = df[df["type"] == "Movie"]
    shows = df[df["type"] == "TV Show"]

    movie_year = movies["release_year"].value_counts().sort_index()
    show_year = shows["release_year"].value_counts().sort_index()

    fig = go.Figure()

    # Add traces (겹쳐 그리기)
    fig.add_trace(go.Scatter(
        x=movie_year.index,
        y=movie_year.values,
        mode="lines",
        name="Movies"
    ))

    fig.add_trace(go.Scatter(
        x=show_year.index,
        y=show_year.values,
        mode="lines",
        name="TV Shows"
    ))

    # Axis & grid 설정
    fig.update_layout(
        title="Netflix Content Trend by Type (Overlay)",
        xaxis_title="Release Year",
        yaxis_title="Number of Titles",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    fig.show()


# subplots
def plot_subplots(df):
    movies = df[df["type"] == "Movie"]
    shows = df[df["type"] == "TV Show"]

    movie_year = movies["release_year"].value_counts().sort_index()
    show_year = shows["release_year"].value_counts().sort_index()

    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Movies Trend", "TV Shows Trend")
    )

    fig.add_trace(
        go.Scatter(
            x=movie_year.index,
            y=movie_year.values,
            mode="lines+markers",
            name="Movies"
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=show_year.index,
            y=show_year.values,
            mode="lines+markers",
            name="TV Shows"
        ),
        row=2,
        col=1
    )

    # Axis & grid 설정
    fig.update_layout(
        title="Netflix Content Trend (Subplots)",
        xaxis_title="Release Year",
        yaxis_title="Number of Titles",
        showlegend=False
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    fig.show()


def main():
    df = load_data()

    plot_overlay(df)
    plot_subplots(df)


if __name__ == "__main__":
    main()
