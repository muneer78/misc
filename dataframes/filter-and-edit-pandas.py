import pandas as pd

df = pd.read_excel(
    "https://github.com/chris1610/pbpython/blob/master/data/sample-sales-reps.xlsx?raw=true"
)

df["commission"] = 0.02
df.loc[df["category"] == "Shirt", ["commission"]] = 0.025
df.loc[(df["category"] == "Belt") & (df["quantity"] >= 10), ["commission"]] = 0.04
df["bonus"] = 0
df.loc[
    (df["category"] == "Shoes") & (df["ext price"] >= 1000), ["bonus", "commission"]
] = 250, 0.045

#  Calculate the compensation for each row
df["comp"] = df["commission"] * df["ext price"] + df["bonus"]

# Summarize and round the results by sales rep
df.groupby(["sales rep"])["comp"].sum().round(2)
