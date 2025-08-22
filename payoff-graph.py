import pandas as pd

df = pd.read_csv("allruns.csv")

df2 = []
df2 = df["Payment Date"].value_counts()

df2.to_csv("payofftotals.csv")
