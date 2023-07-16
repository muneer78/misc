import pandas as pd
import numpy as np

df = pd.read_csv("ars.csv")

df["ARInt"] = df["Account Relationship Name"].str.extract("(\d*\.?\d+)", expand=True)

df["ARNameInt"] = df["Account Relationship Member Name"].str.extract(
    "(\d*\.?\d+)", expand=True
)

df[["ARInt", "ARNameInt"]] = df[["ARInt", "ARNameInt"]].astype(int)

(
    df.groupby(level=0)
    .apply(lambda group: group.nlargest(1, columns="ARInt"))
    .reset_index(level=-1, drop=True)
)

df1 = df.groupby("ARInt", sort=False).apply(
    lambda x: x.reset_index(drop=True).iloc[
        : x.reset_index(drop=True).ARInt.idxmax() + 1, :
    ]
)

df1.to_csv("armaxes.csv")
