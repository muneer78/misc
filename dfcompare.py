import pandas as pd

def load_and_sort_csv(file_name):
    df = pd.read_csv(file_name)
    df_sorted = df.sort_values(by=['nk_dotnbr'])
    return df_sorted

def find_diff_rows(df1, df2):
    comparison_result = df1.ne(df2)
    diff_indices = comparison_result.any(axis=1)
    return df1[diff_indices]

# Load and sort leads data
df_leads = load_and_sort_csv('2023-08-17-Day91Leads.csv')
df_leads_old = load_and_sort_csv('20230815-Day91Leads.csv')

# Find rows with differences in leads dataframes
leads_diff = find_diff_rows(df_leads, df_leads_old)

# Load and sort new opportunities data
df_newopps = load_and_sort_csv('2023-08-17-Day91NewOpps.csv')
df_newopps_old = load_and_sort_csv('20230815-Day91NewOpps.csv')

# Find rows with differences in new opportunities dataframes
newopps_diff = find_diff_rows(df_newopps, df_newopps_old)

# Load and sort reassign opportunities data
df_reassignops = load_and_sort_csv('2023-08-17-Day91ReassignOpps.csv')
df_reassignops_old = load_and_sort_csv('20230815-Day91ReassignOpps.csv')

# Find rows with differences in reassign opportunities dataframes
reassignopps_diff = find_diff_rows(df_reassignops, df_reassignops_old)

# Create Excel writer using context manager
output_file = 'differences_output.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    leads_diff.to_excel(writer, sheet_name='Leads Differences', index=False)
    newopps_diff.to_excel(writer, sheet_name='New Opps Differences', index=False)
    reassignopps_diff.to_excel(writer, sheet_name='Reassign Opps Differences', index=False)

print(f"Differences saved to {output_file}")
