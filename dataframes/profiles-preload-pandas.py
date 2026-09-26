import pandas as pd
from datetime import datetime
from ydata_profiling import ProfileReport
from skimpy import skim
import glob

# Get today's date in the desired format (assuming YYYY-MM-DD)
today_date = datetime.today().strftime("%Y-%m-%d")


def find_file(pattern):
    files = glob.glob("*.csv")
    for f in files:
        if pattern in f:
            return f


# Construct the filenames
leads_filename = find_file("Day91Leads")
newopps_filename = find_file("Day91NewOpps")
reassignopps_filename = find_file("Day91ReassignOpps")

# Create a dictionary to store DataFrames for each CSV file
csv_files = {
    "Leads": leads_filename,
    "New Opps": newopps_filename,
    "Reassign Opps": reassignopps_filename,
}

# Load actual lead uploaded data
df_leads = pd.read_csv(leads_filename)
df_leads = df_leads.dropna(axis=1, how="all")
counts1 = (
    df_leads["rep"].value_counts().sort_values(ascending=False)
)  # Sort in descending order
profile_leads = ProfileReport(df_leads, title="Leads Profiling Report")

# Load new opportunities data
df_newopps = pd.read_csv(newopps_filename)
df_newopps = df_newopps.dropna(axis=1, how="all")
profile_newopps = ProfileReport(df_newopps, title="New Opps Profiling Report")
counts2 = (
    df_newopps["rep"].value_counts().sort_values(ascending=False)
)  # Sort in descending order

# Load reassign opportunities data
df_reassignopps = pd.read_csv(reassignopps_filename)
df_reassignopps = df_reassignopps.dropna(axis=1, how="all")
profile_reassignopps = ProfileReport(
    df_reassignopps, title="Reassign Ops Profiling Report"
)
counts3 = (
    df_reassignopps["rep"].value_counts().sort_values(ascending=False)
)  # Sort in descending order

skim(df_leads)
skim(df_newopps)

# Create profile reports and save them to HTML files
for sheet_name, filename in csv_files.items():
    df = pd.read_csv(filename)  # Load the CSV file
    profile = ProfileReport(df, title=f"{sheet_name} Profiling Report")
    profile.to_file(f"{sheet_name.replace(' ', '_')}.html")


def group_by_rep(df):
    grouped_df = df.groupby("rep").size().reset_index(name="count")
    grouped_df = grouped_df.sort_values(
        by="count", ascending=False
    )  # Sort by count in descending order
    return grouped_df


def write_dataframe_with_title(writer, df, title, sheet_name, start_row, start_col):
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
grouped_leads = group_by_rep(df_leads)
grouped_newopps = group_by_rep(df_newopps)
grouped_reassignopps = group_by_rep(df_reassignopps)

# Create Excel writer using context manager
output_file = f"rep_assign_counts_{today_date}.xlsx"
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    # Write dataframes with titles and empty columns
    write_dataframe_with_title(
        writer, grouped_leads, "Grouped Leads Dataframe", "Lead Assignments", 0, 0
    )
    write_dataframe_with_title(
        writer,
        grouped_newopps,
        "Grouped New Opps Dataframe",
        "New Opps Assignments",
        0,
        0,
    )
    write_dataframe_with_title(
        writer,
        grouped_reassignopps,
        "Grouped Reassign Opps Dataframe",
        "Reassign Opps Assignments",
        0,
        0,
    )

print("Charts are created")
