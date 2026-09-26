import polars as pl
import pandas as pd
from datetime import datetime as dt

# Get the current date
current_date = dt.now()

# Read the CSV file
df = pl.read_csv("DS4013-20240605.csv")

# Create 'cleanedclientno' column by removing non-numeric characters from 'clientno'
df = df.with_columns(
    pl.col("clientno").str.replace_all(r"\D", "").alias("cleanedclientno")
)


# Function to create a grouped DataFrame
def create_grouped_df(df, column_name):
    return (
        df.group_by(column_name)
        .agg(pl.col(column_name).count().alias("count"))
        .sort("count", descending=True)
    )


# Columns to analyze
columns = ["cleanedclientno", "acctexec", "masterclientkey"]

ticket_number = "insert Jira number here"
output_filename = f"DS{ticket_number}_{current_date}_output.xlsx"

# Create a Pandas Excel writer using Openpyxl
with pd.ExcelWriter(output_filename, engine="openpyxl") as writer:
    for column in columns:
        # Create grouped DataFrame
        grouped_df = create_grouped_df(df, column)

        # Convert grouped DataFrame to Pandas DataFrame for Excel writing
        pandas_df = grouped_df.to_pandas()

        # Write the DataFrame to a new sheet
        pandas_df.to_excel(writer, sheet_name=f"{column}_counts", index=False)

        # Load the workbook and add the image to the corresponding sheet
        workbook = writer.book
        worksheet = workbook[f"{column}_counts"]

print("Dataframes have been created and saved to charts.xlsx")
