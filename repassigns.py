import pandas as pd
from datetime import datetime

def load_and_sort_csv(file_name):
    df = pd.read_csv(file_name)
    df_sorted = df.sort_values(by=['nk_dotnbr'])
    return df_sorted

def group_by_rep(df):
    grouped_df = df.groupby('rep').size().reset_index(name='count')
    grouped_df = grouped_df.sort_values(by='count', ascending=False)  # Sort by count in descending order
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
today_date = datetime.today().strftime('%Y-%m-%d')  # Get today's date in 'YYYY-MM-DD' format
df_leads = load_and_sort_csv(f'{today_date}-Day91Leads.csv')
df_newopps = load_and_sort_csv(f'{today_date}-Day91NewOpps.csv')
df_reassignops = load_and_sort_csv(f'{today_date}-Day91ReassignOpps.csv')

# Group the dataframes by 'rep' column and sort in descending order of 'count'
grouped_leads = group_by_rep(df_leads)
grouped_newopps = group_by_rep(df_newopps)
grouped_reassignops = group_by_rep(df_reassignops)

# Create Excel writer using context manager
output_file = f'rep_assign_counts_{today_date}.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    # Write dataframes with titles and empty columns
    write_dataframe_with_title(writer, grouped_leads, "Grouped Leads Dataframe", "Sheet1", 2, 1)
    write_dataframe_with_title(writer, grouped_newopps, "Grouped New Opps Dataframe", "Sheet2", 2, 1)
    write_dataframe_with_title(writer, grouped_reassignops, "Grouped Reassign Opps Dataframe", "Sheet3", 2, 1)

print(f"Dataframes saved to {output_file}")
