import pandas as pd
from pathlib import Path
import plotly.express as px


# load
def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "netflix_titles.csv"
    return pd.read_csv(data_path)


# bar chart
def plot_content_type_distribution(df):
    type_count = df["type"].value_counts().reset_index()
    type_count.columns = ["type", "count"]

    fig = px.bar(
        type_count,
        x="type",
        y="count",
        title="Distribution of Content Types on Netflix"
    )

    # Trace update
    fig.update_traces(
        marker_color="steelblue",
        text=type_count["count"],
        textposition="outside"
    )

    fig.show()


# line chart
def plot_release_trend(df):
    yearly_count = (
        df.groupby("release_year")
          .size()
          .reset_index(name="count")
          .sort_values("release_year")
    )

    fig = px.line(
        yearly_count,
        x="release_year",
        y="count",
        title="Number of Netflix Titles by Release Year"
    )

    # Trace update
    fig.update_traces(
        line=dict(width=3),
        mode="lines+markers",
        marker=dict(size=6)
    )

    fig.show()


# histogram
def plot_duration_distribution(df):
    movies = df[df["type"] == "Movie"].copy()
    movies["duration_min"] = movies["duration"].str.extract(r"(\d+)").astype(float)

    fig = px.histogram(
        movies,
        x="duration_min",
        nbins=30,
        title="Movie Duration Distribution (Minutes)"
    )

    # Trace update
    fig.update_traces(
        marker_color="orange",
        opacity=0.75
    )

    fig.show()



def main():
    df = load_data()

    plot_content_type_distribution(df)
    plot_release_trend(df)
    plot_duration_distribution(df)


if __name__ == "__main__":
    main()
