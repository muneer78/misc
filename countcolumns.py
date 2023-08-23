import pandas as pd

pd.set_option('display.max_columns', None)
df = pd.read_csv('dataset.csv', header=0)

output=df.count(axis=0, level=None, numeric_only=False)

output.to_csv('result.csv', index=False)
