import polars as pl
from rich import print

# Assuming df_cadenceold and df_cadencenew are your DataFrames
df = pl.read_csv(
    "part-00000-tid-2659363838259475703-6031fdb8-b31c-4691-9047-fe28ed7dd359-4-1-c000.csv"
)

print(df.columns)

print(df.head)
