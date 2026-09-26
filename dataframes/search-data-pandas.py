"""
This code can optimize searching for a couple of records in a huge dataset.
"""

import pandas as pd

# Read the CSV file into a DataFrame
df_alldata = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\cadence_mra_compliance_sf_2025-03-01000.csv"
)

search_items = {"records": ["0011H00001nbw7rQAA", "0013x00002Rt8efAAB"]}
df_searchitems = pd.DataFrame(data=search_items)

# Define the search items from the 'col1' column of df_searchitems as a set
search_items = set(df_searchitems["records"])

# Define a set comprehension to filter rows in df_alldata
filtered_data = df_alldata[df_alldata["original_search_column"].isin(search_items)]

# Print alll columns of the filtered data
print(filtered_data.to_string())
