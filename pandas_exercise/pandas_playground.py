import pandas as pd
from pathlib import Path


# load 
def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "netflix_titles.csv"
    return pd.read_csv(data_path)


# insert()
def insert_column(df):
    df = df.copy()
    df.insert(
        loc=2,
        column="title_length",
        value=df["title"].str.len()
    )
    print("\n[insert()]")
    print(df[["title", "title_length"]].head())
    return df


# pop()
def pop_column(df):
    df = df.copy()
    popped = df.pop("rating")
    print("\n[pop()]")
    print("Remaining columns:", df.columns.tolist())
    print("Popped values:")
    print(popped.head())
    return df


# copy()
def copy_dataframe(df):
    df_copy = df.copy()
    df_copy["release_year"] += 1

    print("\n[copy()]")
    print("Original release_year:")
    print(df["release_year"].head())

    print("Copied & modified release_year:")
    print(df_copy["release_year"].head())

    return df_copy


# drop() and truncate()
def drop_and_truncate(df):
    df_dropped = df.drop(columns=["country"], errors="ignore")

    print("\n[drop()]")
    print(df_dropped.columns)

    df_truncated = df.truncate(before=10, after=20)

    print("\n[truncate()]")
    print(df_truncated)

    return df_dropped, df_truncated


# concat()
def concat_dataframes(df):
    movies = df[df["type"] == "Movie"].head(3)
    shows = df[df["type"] == "TV Show"].head(3)

    combined = pd.concat([movies, shows], axis=0)

    print("\n[concat()]")
    print(combined[["type", "title"]])

    return combined


# drop_duplicates()
def remove_duplicates(df):
    deduplicated = df.drop_duplicates(subset=["title", "type"])

    print("\n[drop_duplicates()]")
    print("Before:", len(df))
    print("After :", len(deduplicated))

    return deduplicated


def main():
    df = load_data()

    print("Original Data:")
    print(df.head())

    df = insert_column(df)
    df = pop_column(df)
    copy_dataframe(df)
    drop_and_truncate(df)
    concat_dataframes(df)
    remove_duplicates(df)


if __name__ == "__main__":
    main()
