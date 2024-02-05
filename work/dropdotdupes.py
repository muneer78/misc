import pandas as pd

df = pd.read_csv("DOTandMCExceptionsFile.csv")

# Assuming df is your DataFrame
df.drop_duplicates(subset="UID", keep="first", inplace=True)

df.to_csv("DOTandMCExceptionsFile.csv", index=False)
