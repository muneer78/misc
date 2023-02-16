import pandas as pd

df = pd.read_csv("fg.csv")
df1 = pd.read_csv("bbref.csv")

df = df.replace(r'[^\w\s]|_\*', '', regex=True)
df1 = df1.replace(r'[^\w\s]|_\*', '', regex=True)

func = lambda x: ''.join([i[:3] for i in x.strip().split(' ')])
df['Key']=df.Name.apply(func)

func = lambda x: ''.join([i[:3] for i in x.strip().split(' ')])
df1['Key']=df1.Name.apply(func)

df.columns = df.columns.str.strip()
df1.columns = df1.columns.str.strip()
