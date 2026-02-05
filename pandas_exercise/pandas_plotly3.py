import pandas as pd
from pathlib import Path
import plotly.io as pio

# backend
pd.options.plotting.backend = "plotly"


# load
def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "netflix_titles.csv"
    return pd.read_csv(data_path)

# template 1
def plot_top_countries(df):
    import plotly.io as pio
    pio.templates.default = "plotly_dark"

    # country column sometimes has multiple countries
    country_series = (
        df["country"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    top_countries = (
        country_series.value_counts()
        .head(10)
        .reset_index()
    )

    top_countries.columns = ["country", "count"]

    fig = top_countries.plot(
        x="country",
        y="count",
        kind="bar",
        title="Top 10 Countries by Netflix Content"
    )

    fig.update_layout(hovermode="x unified")

    fig.show()

# legend 
def plot_movie_tv_trend(df):
    import plotly.io as pio
    pio.templates.default = "presentation"

    trend = (
        df.groupby(["release_year", "type"])
          .size()
          .reset_index(name="count")
    )

    pivot = trend.pivot(
        index="release_year",
        columns="type",
        values="count"
    ).fillna(0)

    fig = pivot.plot(
        kind="line",
        title="Movie vs TV Show Trend Over Time"
    )

    # legend layout
    fig.update_layout(
        legend=dict(
            title="Content Type",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(0,0,0,0)",
            borderwidth=1
        )
    )

    fig.show()

# template 2
def plot_release_vs_duration(df):
    import plotly.io as pio
    pio.templates.default = "ggplot2"

    scatter_df = df.copy()

    # extract numeric duration
    scatter_df["duration_num"] = (
        scatter_df["duration"]
        .str.extract(r"(\d+)")
        .astype(float)
    )

    scatter_df = scatter_df.dropna(
        subset=["release_year", "duration_num"]
    )

    fig = scatter_df.plot(
        x="release_year",
        y="duration_num",
        kind="scatter",
        title="Release Year vs Duration"
    )

    fig.update_layout(hovermode="closest")

    fig.show()



def main():
    df = load_data()

    plot_top_countries(df)
    plot_movie_tv_trend(df)
    plot_release_vs_duration(df)


if __name__ == "__main__":
    main()
