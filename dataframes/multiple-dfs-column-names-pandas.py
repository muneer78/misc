import pandas as pd

# Step 1: Read CSV files
df_bidata = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\rpl_task_202411111348.csv"
)
df_sf_task = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\salesforce_opty_task_pushouts_202411111348.csv"
)

# Step 2: Extract headers (column names) from both DataFrames and add a 'Source' label for each row
header1 = pd.DataFrame({"col-name": df_bidata.columns, "source": "bidata"})
header2 = pd.DataFrame({"col-name": df_sf_task.columns, "source": "sf"})

# Step 3: Concatenate headers into a single DataFrame
final_headers = pd.concat([header1, header2], ignore_index=True)

final = final_headers.sort_values("col-name")

# Step 4: Write the result to a new CSV file
final.to_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\code\header-compare.csv", index=False
)

print("Headers have been written to 'header-compare.csv'.")
