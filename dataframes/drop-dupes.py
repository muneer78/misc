import pandas as pd

df = pd.read_csv("draftsheet2.csv")

df = df.drop_duplicates(subset=["Player", "Rank"], keep="last")

df.to_csv("draftsheetfinal.csv")
