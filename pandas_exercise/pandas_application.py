import pandas as pd
from pathlib import Path

def load_stock_data():
    # Load Kaggle stock CSV using base directory path.
    # CSV is expected at: data/data.csv
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "data" / "AMZN.csv"

    print("Loading stock data from:", csv_path)

    df = pd.read_csv(csv_path)
    return df


def run_examples(df):
    print("\n=== PandAS Merge / Join / Combine / Sort Examples ===")

    # merge 
    # Create a small earnings dataframe (simulated)
    earnings_df = pd.DataFrame({
        "Date": df["Date"].iloc[:10],
        "EarningsFlag": ["Beat", "Miss", "Beat", "Beat", "Miss",
                         "Beat", "Beat", "Miss", "Beat", "Beat"]
    })

    merged_df = pd.merge(df, earnings_df, on="Date", how="left")
    print("\n[merge()] Result:")
    print(merged_df[["Date", "Close", "EarningsFlag"]].head(10))

    # join
    volume_df = df[["Date", "Volume"]].iloc[:10].copy()
    volume_df = volume_df.set_index("Date")

    price_df = df[["Date", "Close"]].iloc[:10].copy()
    price_df = price_df.set_index("Date")

    joined_df = price_df.join(volume_df)
    print("\n[join()] Result (index-based):")
    print(joined_df.head())

    # combine
    # Compare Close vs Open and take max per row
    open_series = df["Open"].iloc[:10]
    close_series = df["Close"].iloc[:10]

    combined_series = open_series.combine(close_series, func=max)
    print("\n[combine()] Result (max of Open vs Close):")
    print(combined_series.head(10))


    # sort_values() + head()
    top_volume_days = df.sort_values(by="Volume", ascending=False).head(5)
    print("\n[sort_values + head()] Top 5 Volume Days:")
    print(top_volume_days[["Date", "Volume"]])

    # sorting
    # value-based sort
    sorted_by_close = df.sort_values(by="Close", ascending=True).head(5)
    print("\n[sort_values()] Lowest 5 Close Prices:")
    print(sorted_by_close[["Date", "Close"]])

    # index-based sort
    index_sorted = df.set_index("Date").sort_index().head(5)
    print("\n[sort_index()] Date Index Sorted:")
    print(index_sorted[["Close", "Volume"]])

def main():
    # Load CSV
    df = load_stock_data()
    run_examples(df)

if __name__ == "__main__":
    main()