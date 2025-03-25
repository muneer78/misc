import pandas as pd

df=pd.read_clipboard()

print(df)

output=df.to_csv('enobounceback.csv')