import pandas as pd

# Load actual lead uploaded data
df = pd.read_csv("df.csv")

# Create a pivot table
pivot_df = pd.pivot_table(
    df, values="column", index="rep", aggfunc="count"
).reset_index()
pivot_df = pivot_df.sort_values(by="count", ascending=False)

# Save to Excel
pivot_df.to_excel("pivot_table.xlsx", index=False)
