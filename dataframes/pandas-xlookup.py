import pandas as pd
import csv

df1 = pd.read_excel("file.xlsx", sheet_name="Master File")
df2 = pd.read_csv("file.csv")


def xlookup(lookup_value, lookup_array, return_array, if_not_found: str = None):
    match_value = return_array.loc[lookup_array == lookup_value]

    if match_value.empty:
        return if_not_found

    else:
        return match_value.tolist()[0]


df1 = df1[df1["lookup"].notna()]

df1["return"] = df1["lookup"].apply(xlookup, args=(df2["lookup"], df2["returnmatch"]))

columns = ["lookup", "return"]

with open("users.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    for index, row in df1.iterrows():
        if pd.isnull(row["return"]):
            continue  # skip row if Bundle Type is null
        writer.writerow([row["lookup"], row["return"]])
