import pandas as pd

def load_and_sort_csv(file_name):
    df = pd.read_csv(file_name)
    df_sorted = df.sort_values(by=['nk_dotnbr'])
    return df_sorted

def group_by_rep(df):
    grouped_df = df.groupby('rep').size().reset_index(name='count')
    return grouped_df

def write_dataframe_with_title(writer, df, title, sheet_name, start_row, start_col):
    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=start_row, startcol=start_col)
    worksheet = writer.sheets[sheet_name]  # Get the current worksheet
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(start_row, start_col + col_num, value)
        col_width = max(
            df[value].astype(str).str.len().max(),
            len(str(value))  # Account for the width of the column header
        ) + 2
        worksheet.set_column(start_col + col_num, start_col + col_num, col_width)

# Load and sort data
df_leads = load_and_sort_csv('2023-08-21-Day91Leads.csv')
df_leads_old = load_and_sort_csv('20230821-Day91Leads-old.csv')
df_newopps = load_and_sort_csv('2023-08-21-Day91NewOpps.csv')
df_newopps_old = load_and_sort_csv('20230821-Day91NewOpps-old.csv')
df_reassignops = load_and_sort_csv('2023-08-21-Day91ReassignOpps.csv')
df_reassignops_old = load_and_sort_csv('20230821-Day91ReassignOpps-old.csv')

# Group the dataframes by 'rep' column
grouped_leads = group_by_rep(df_leads)
grouped_leads_old = group_by_rep(df_leads_old)
grouped_newopps = group_by_rep(df_newopps)
grouped_newopps_old = group_by_rep(df_newopps_old)
grouped_reassignops = group_by_rep(df_reassignops)
grouped_reassignops_old = group_by_rep(df_reassignops_old)

# Create Excel writer using context manager
output_file = 'grouped_output.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    # Write dataframes with titles and empty columns
    write_dataframe_with_title(writer, grouped_leads, "Grouped Leads Dataframe", "Sheet1", 2, 1)
    write_dataframe_with_title(writer, grouped_leads_old, "Grouped Old Leads Dataframe", "Sheet1", 2, grouped_leads.shape[1] + 4)
    write_dataframe_with_title(writer, grouped_newopps, "Grouped New Opps Dataframe", "Sheet2", 2, 1)
    write_dataframe_with_title(writer, grouped_newopps_old, "Grouped Old New Opps Dataframe", "Sheet2", 2, grouped_newopps.shape[1] + 4)
    write_dataframe_with_title(writer, grouped_reassignops, "Grouped Reassign Opps Dataframe", "Sheet3", 2, 1)
    write_dataframe_with_title(writer, grouped_reassignops_old, "Grouped Old Reassign Opps Dataframe", "Sheet3", 2, grouped_reassignops.shape[1] + 4)

print(f"Dataframes saved to {output_file}")
