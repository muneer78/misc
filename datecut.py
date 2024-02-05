import pandas as pd

df = pd.read_csv("DOTAcctsProcessed.csv")

# Assuming your DataFrame is named 'df' and has a column 'DateProcessed'
df["DateProcessed"] = df["DateProcessed"].str.replace(" 12:00:00 AM", "")

df.to_csv("DOTAcctsProcessed.csv", index=False)
