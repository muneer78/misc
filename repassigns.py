import pandas as pd

def load_and_sort_csv(file_name):
    df = pd.read_csv(file_name)
    df_sorted = df.sort_values(by=['nk_dotnbr'])
    return df_sorted

def group_by_rep(df):
    grouped_df = df.groupby('rep').size().reset_index(name='count')
    return grouped_df

def write_dataframe_with_title(writer, df, title, sheet_name):
    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=2)
    # Set column width for better visualization
    worksheet = writer.sheets["Sheet1"]
    for col_num, value in enumerate(grouped_leads.columns.values):
        worksheet.write(1, col_num, value)
        col_width = max(
            grouped_leads[value].astype(str).str.len().max(),
            grouped_leads_old[value].astype(str).str.len().max(),
            len(str(value))  # Account for the width of the column header
    ) + 2
        worksheet.set_column(col_num, col_num, col_width)
# Load and sort data
df_leads = load_and_sort_csv('2023-08-17-Day91Leads.csv')
df_leads_old = load_and_sort_csv('20230815-Day91Leads.csv')
df_newopps = load_and_sort_csv('2023-08-17-Day91NewOpps.csv')
df_newopps_old = load_and_sort_csv('20230815-Day91NewOpps.csv')
df_reassignops = load_and_sort_csv('2023-08-17-Day91ReassignOpps.csv')
df_reassignops_old = load_and_sort_csv('20230815-Day91ReassignOpps.csv')

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
    write_dataframe_with_title(writer, grouped_leads, "Grouped Leads Dataframe", "Sheet1")
    write_dataframe_with_title(writer, grouped_leads_old, "Grouped Old Leads Dataframe", "Sheet1")
    write_dataframe_with_title(writer, grouped_newopps, "Grouped New Opps Dataframe", "Sheet2")
    write_dataframe_with_title(writer, grouped_newopps_old, "Grouped Old New Opps Dataframe", "Sheet2")
    write_dataframe_with_title(writer, grouped_reassignops, "Grouped Reassign Opps Dataframe", "Sheet3")
    write_dataframe_with_title(writer, grouped_reassignops_old, "Grouped Old Reassign Opps Dataframe", "Sheet3")

print(f"Dataframes saved to {output_file}")
