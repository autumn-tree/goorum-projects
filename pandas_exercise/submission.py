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


def main():
    # Load CSV
    df = load_stock_data()

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    print("Original Stock Data:")
    print(df.head())

    # Calculate Exponentially Weighted Moving Average
    df["EWM_10"] = df["Close"].ewm(span=10, adjust=False).mean()
    df["EWM_30"] = df["Close"].ewm(span=30, adjust=False).mean()

    print("\nWith EWM Columns:")
    print(df[["Date", "Close", "EWM_10", "EWM_30"]].head(15))


if __name__ == "__main__":
    main()
