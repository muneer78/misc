import pandas as pd

df = pd.read_csv('draftsheet.csv')
df1 = pd.read_csv('sleepers.csv')

df2 = df.merge(df1[['Player', 'Sleeper Count', 'Overrated Count', 'Experts']], on=["Player"], how="inner")
df2 = df2.drop_duplicates(subset=['Player', 'Rank'], keep='last')

df2 = df2.to_csv('finaldraftsheet.csv')