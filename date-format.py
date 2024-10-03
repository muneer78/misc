import pandas as pd

df = pd.read_csv("DOTAcctsProcessed.csv")

import pandas as pd

# # Assuming your DataFrame is named 'df' and has a column 'DateProcessed'
# df["DateProcessed"] = pd.to_datetime(df["DateProcessed"]).dt.strftime("%m/%d/%Y")

df["DateProcessed"] = pd.to_datetime(df["DateProcessed"], format="mixed").dt.strftime(
    "%m/%d/%Y"
)

df.to_csv("DOTAcctsProcessed.csv", index=False)
