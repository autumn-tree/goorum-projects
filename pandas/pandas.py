import pandas as pd

df1 = pd.DataFrame({
    "A": [10, 20, 30],
    "B": [5, 10, 15]
})

df2 = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [2, 4, 6]
})

print("DataFrame 1:")
print(df1)

print("\nDataFrame 2:")
print(df2)

df1["A_plus_10"] = df1["A"] + 10
df1["B_times_2"] = df1["B"] * 2

print("\nAdjusted DataFrame 1:")
print(df1)


add_df = df1[["A", "B"]] + df2
sub_df = df1[["A", "B"]] - df2
mul_df = df1[["A", "B"]] * df2
div_df = df1[["A", "B"]] / df2

print("\nAddition (df1 + df2):")
print(add_df)

print("\nSubtraction (df1 - df2):")
print(sub_df)

print("\nMultiplication (df1 * df2):")
print(mul_df)

print("\nDivision (df1 / df2):")
print(div_df)
