import pandas as pd
import numpy as np

df = pd.read_excel("sample-salesv3.xlsx")

df["name"].unique()

# Drop any records in the second field that are dupes and only select 1st 2 columns in dataframe
df.drop_duplicates(subset=["account number", "name"]).iloc[:, [0, 1]]
