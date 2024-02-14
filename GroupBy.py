import pandas as pd

df = pd.read_csv("System Closed Opps with Score Workbook.csv")

# grouped_df = df["STC Lead Score"].value_counts()

grouped_df = (
    df.groupby("STC Lead Score")["STC Lead Score"].count().sort_values(ascending=False)
)

print(grouped_df)
