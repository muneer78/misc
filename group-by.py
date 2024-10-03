import pandas as pd

df = pd.read_csv("System Closed Opps with Score Workbook.csv")

grouped_df = df["STC Lead Score"].value_counts().reset_index(name="Number")

print(grouped_df)

grouped_df.to_csv("GroupedDF.csv", index=False)
