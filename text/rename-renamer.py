import os
import pandas as pd

df = pd.read_csv("data.csv")


for old, new in zip(df["OldName"], df["NewName"]):
    try:
        os.rename(old, new)
    except OSError as exc:
        print(f"WARNING: could not rename {old} to {new}: {exc}")
    else:
        print(f"renamed {old} to {new}")
