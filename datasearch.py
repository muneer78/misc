'''
This code can optimize searching for a couple of records in a huge dataset.
'''

import pandas as pd

# Read the CSV file into a DataFrame
df_alldata = pd.read_csv('bigdataset.csv')

search_items = {'records': ['Item1', 'Item2']}
df_searchitems = pd.DataFrame(data=search_items)

# Define the search items from the 'col1' column of df_searchitems as a set
search_items = set(df_searchitems['records'])

# Define a set comprehension to filter rows in df_alldata
filtered_data = df_alldata[df_alldata['original_search_column'].isin(search_items)]

# Print the filtered data
print(filtered_data)
