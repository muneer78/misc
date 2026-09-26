import pandas as pd
from rich import print
from datetime import datetime as dt

# DS4220
date = date = dt.today().strftime("%Y-%m-%d")


def export_data_to_excel(df1_not_in_df2, df2_not_in_df1, date):
    excel_file_name = f"{date}-Diff.xlsx"
    with pd.ExcelWriter(excel_file_name) as writer:
        df1_not_in_df2.to_excel(writer, sheet_name="DF1NotInDF2", index=False)
        df2_not_in_df1.to_excel(writer, sheet_name="DF2NotInDF1", index=False)


df1 = pd.read_csv("DS4220-20240517.csv")
df2 = pd.read_csv("TransactionSummaryLLCGrp_Daily_184835_05-09-2024v2.csv")

# Total records in each df
df1_len = len(df1)
df2_len = len(df2)

print("Count of records in df1:", df1_len)
print("Count of records in df2:", df2_len)

# Count duplicate values in transaction id columns
df1_transid_dupes = len(df1["transid"]) - len(df1["transid"].drop_duplicates())
print("Number of duplicate transaction ids in df1:", df1_transid_dupes)
df2_transid_dupes = len(df2["Trans. Id"]) - len(df2["Trans. Id"].drop_duplicates())
print("Number of duplicate transaction ids in df2:", df2_transid_dupes)

# Count of records that are in df1 but not df2. Drop all duplicates.
df1_not_in_df2 = df1[~df1["transid"].isin(df2["Trans. Id"])].drop_duplicates()
df1_not_in_df2_count = len(
    df1[~df1["transid"].isin(df2["Trans. Id"])].drop_duplicates()
)

# Count of records that are in df2 but not df1. Drop all duplicates.
df2_not_in_df1 = df2[~df2["Trans. Id"].isin(df1["transid"])].drop_duplicates()
df2_not_in_df1_count = len(
    df2[~df2["Trans. Id"].isin(df1["transid"])].drop_duplicates()
)

print("Count of records in df1 but not df2:", df1_not_in_df2_count)
print("Count of records in df2 but not df1:", df2_not_in_df1_count)

export_data_to_excel(df1_not_in_df2, df2_not_in_df1, date)
