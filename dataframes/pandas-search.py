"""
This code can optimize searching for a couple of records in a huge dataset.
"""

import pandas as pd

# Read the CSV file into a DataFrame
df_alldata = pd.read_csv("DS5088_all_records.csv")

search_items = {"col1": ["BUSCH", "BERRY"]}
df_searchitems = pd.DataFrame(data=search_items)

# Define the search items from the 'col1' column of df_searchitems as a set
search_items = set(df_searchitems["col1"])

# Define a set comprehension to filter rows in df_alldata
filtered_data = df_alldata[df_alldata["customer_name"].isin(search_items)]

# Print the filtered data
print(filtered_data)
