import pandas as pd

# 1. Load the data
df = pd.read_csv("data/tickets.csv")

# 2. Size of the data
print("Shape (rows, columns):", df.shape)

# 3. Column names
print("\nColumns:", list(df.columns))

# 4. First few rows
print("\nFirst 5 rows:")
print(df.head())

# 5. Missing values per column
print("\nMissing values:")
print(df.isnull().sum())

# 6. How many tickets in each category
print("\nCategory counts:")
print(df["category"].value_counts())