import pandas as pd

# Sample sales data
data = {
    "region": ["Seoul", "Seoul", "Busan", "Busan", "Seoul"],
    "product": ["A", "B", "A", "B", "A"],
    "sales": [100, 150, 80, 120, 200]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# Groupby with multiple aggregations
grouped = df.groupby(
    by=["region", "product"],
    as_index=False
).agg(
    total_sales=("sales", "sum"),
    avg_sales=("sales", "mean"),
    count=("sales", "count")
)

print("\nGrouped Result:")
print(grouped)

