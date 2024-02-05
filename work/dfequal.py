import pandas as pd

def load_and_sort_csv(file_name):
    df = pd.read_csv(file_name)
    df_sorted = df.sort_values(by=['nk_dotnbr'])
    return df_sorted

def compare_dataframes(df1, df2):
    comparison_result = df1.eq(df2)
    return comparison_result

# Load and sort leads data
df_leads = load_and_sort_csv('2023-08-21-Day91Leads.csv')
df_leads_old = load_and_sort_csv('20230821-Day91Leads-old.csv')

# Compare leads dataframes
leads_equal = compare_dataframes(df_leads, df_leads_old)

# Load and sort new opportunities data
df_newopps = load_and_sort_csv('2023-08-21-Day91NewOpps.csv')
df_newopps_old = load_and_sort_csv('20230821-Day91NewOpps-old.csv')

# Compare new opportunities dataframes
newopps_equal = compare_dataframes(df_newopps, df_newopps_old)

# Load and sort reassign opportunities data
df_reassignops = load_and_sort_csv('2023-08-21-Day91ReassignOpps.csv')
df_reassignops_old = load_and_sort_csv('20230821-Day91ReassignOpps-old.csv')

# Find rows with differences in reassign opportunities dataframes
reassignopps_equal = compare_dataframes(df_reassignops, df_reassignops_old)

# Create Excel writer using context manager
output_file = 'row_level_comparison_output.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    # Write row-level comparisons to separate sheets
    leads_equal.to_excel(writer, sheet_name='Leads Comparison', index=False)
    newopps_equal.to_excel(writer, sheet_name='New Opps Comparison', index=False)
    reassignopps_equal.to_excel(writer, sheet_name='Reassign Opps Comparison', index=False)

print(f"Row-level comparisons saved to {output_file}")