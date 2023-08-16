import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Read data
df_sheets = pd.read_excel('ExcelSheet.xlsx', sheet_name=['Create Sheet 1', 'Create Sheet 2', 'Create Sheet 3'])
df1 = df_sheets.get('Sheet 1')
df2 = df_sheets.get('Sheet 2')

df_dict_values = pd.read_csv('List.csv')
id_dict = dict(zip(df_dict_values.Name, df_dict_values.ID))

# Preprocess df1
df1['assignees'] = None

def set_values(row):
    if row['column a'] > 40:
        return "40+"
    elif row['column b'] == 'Thing A' and row['column a'] <= 5:
        return "AZ 1-5"
    else:
        return "not processed"

df1['assignedvalue1'] = df1.apply(set_values, axis=1)

# Assign values using dictionaries
rep_dict = {
    'Option A': ['abcd'],
    'Option B': ['d', 'e', 'f'],
    'Option C': ['m', 'n', 'o']
}

assigned_reps = {}
for index, row in df1.iterrows():
    bucket = row['assignees']
    values = rep_dict.get(bucket, [])
    if values:
        if bucket not in assigned_reps:
            assigned_reps[bucket] = 0
        assigned_index = assigned_reps[bucket]
        num_assignees = len(values)
        val_index = assigned_index % num_assignees
        row['assignee'] = values[assigned_index]
        row['id'] = id_dict.get(row['id'], "")
        assigned_reps[bucket] += 1
        df1.loc[index] = row

# Filter and reset index
df1_filtered = df1[df1['assignee'] == "y"].copy()
df1_filtered.reset_index(drop=True, inplace=True)

# Modify columns
df1['Column D'] = "No"
df1['Column E'] = "New"

# Save to CSV
date = datetime.now().strftime('%Y%m%d')
df1.to_csv(f'{date}-Dataset.csv', index=False)

# Modify df2
df2['ColumnA'] = None

# Save exceptions to Excel
date2 = datetime.now()
future = date2 + relativedelta(months=1)
future_str = future.strftime("%m/%d/%Y")

with pd.ExcelWriter(f'{date}-Exceptions.xlsx') as writer:
    df2.to_excel(writer, sheet_name='Opportunities', index=False)

# Read result data
df_result = pd.read_csv('result.csv')

# Merge and save final results
success_results = pd.merge(df_result, df1, left_on='name', right_on=["other_name"])
success_results.drop('other_name', axis=1, inplace=True)

with pd.ExcelWriter(f'{date}-FinalFile.xlsx') as writer:
    success_results.to_excel(writer, sheet_name='Sheet1', index=False)
    df2.to_excel(writer, sheet_name='Sheet2', index=False)
