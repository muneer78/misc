import pandas as pd

df=pd.read_csv("fg.csv")

func = lambda x: ''.join([i[:3] for i in x.strip().split(' ')])
df['Key']=df.Name.apply(func)

df.to_csv('newfg.csv']