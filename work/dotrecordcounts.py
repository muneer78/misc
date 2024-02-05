import pandas as pd
from datetime import datetime

# Load the CSV file into a DataFrame
df = pd.read_csv("DOTAcctsProcessed.csv")

# Convert the "DateProcessed" column to datetime format
df["DateProcessed"] = pd.to_datetime(df["DateProcessed"])

# Format the "DateProcessed" column to the desired format "M/d/Y"
df["DateProcessed"] = df["DateProcessed"].dt.strftime("%m/%d/%Y")

# Get today's date in the desired format (assuming YYYY-MM-DD)
today_date = datetime.today().strftime("%Y-%m-%d")

counts1 = (
    df["DateProcessed"].value_counts().sort_index(ascending=False)
)  # Sort by date in descending order


def group_by_date(df):
    grouped_df = df.groupby("DateProcessed").size().reset_index(name="count")
    grouped_df = grouped_df.sort_values(
        by=["DateProcessed", "count"], ascending=[True, False]
    )  # Sort by DateProcessed in ascending order, and then by count in descending order
    return grouped_df


def write_dataframe_with_title(writer, df, sheet_name, start_row, start_col):
    df.to_excel(
        writer,
        sheet_name=sheet_name,
        index=False,
        startrow=start_row,
        startcol=start_col,
    )
    worksheet = writer.sheets[sheet_name]  # Get the current worksheet
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(start_row, start_col + col_num, value)
        col_width = (
            max(
                df[value].astype(str).str.len().max(),
                len(str(value)),  # Account for the width of the column header
            )
            + 2
        )
        worksheet.set_column(start_col + col_num, start_col + col_num, col_width)


# Group the dataframes by 'rep' column and sort in descending order of 'count'
grouped = group_by_date(df)

# Print sorted counts to terminal
print("Sorted counts by DateProcessed:")
print(grouped)

# Print grand total
grand_total = grouped["count"].sum()
print(f"Grand Total: {grand_total}")

# Create Excel writer using context manager
output_file = f"dot_counts_{today_date}.xlsx"
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    # Write dataframes with titles and empty columns
    write_dataframe_with_title(writer, grouped, "Counts", "Totals", 0, 0)
