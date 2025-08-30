"""
Using pandas to create dataframe
"""

import pandas as pd

pd.set_option("display.max_columns", None)
df = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\search\part-00000-tid-6380730436421644697-fbe9cfda-ce89-431b-b57f-883e9ba807ae-1104-1-c000.csv",
    header=0,
)

output = df.count()

print("Total rows:", len(df))
# output.to_csv("result.csv", index=False)
