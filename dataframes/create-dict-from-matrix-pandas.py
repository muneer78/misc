# import pandas as pd
# import csv

# # Load the Excel file containing the matrix
# df_input = pd.read_excel('Seed Records.xlsx', header=None)

# # Initialize an empty dictionary to store the key-value pairs
# key_value_pairs = {}

# # Iterate over the rows and columns to create the key-value pairs
# for i in range(1, 17):  # Row index
#     for j in range(1, 17):  # Column index
#         # Create keys in the format 'row-column' and 'column-row'
#         key1 = f"{i}-{j}"
#         key2 = f"{j}-{i}"
#         # Retrieve the value at the intersection of the current row and column
#         value = df_input.iloc[i, j]
#         # Add key-value pairs to the dictionary
#         key_value_pairs[key1] = value
#         key_value_pairs[key2] = value

# # Write the key-value pairs to a CSV file
# with open('seedrecords.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Key', 'Value'])  # Write header
#     for key, value in key_value_pairs.items():
#         writer.writerow([key, value])

import pandas as pd

# Load the Excel file containing the matrix
df_input = pd.read_excel("Seed Records.xlsx", header=None)

# Initialize empty dictionaries to store the key-value pairs for column-row and row-column
column_row_pairs = {}
row_column_pairs = {}

# Iterate over the rows and columns to create the key-value pairs for column-row
for i in range(1, 17):  # Row index
    column_values = df_input.iloc[i].tolist()
    for j, value in enumerate(column_values, start=0):  # Column index starts from 1
        key = f"{i}-{j}"  # Format: column-row
        column_row_pairs[key] = value

# Iterate over the rows and columns to create the key-value pairs for row-column
for i in range(1, 17):  # Row index
    row_values = df_input.iloc[:, i].tolist()
    for j, value in enumerate(row_values, start=0):  # Row index starts from 1
        key = f"{j}-{i}"  # Format: row-column
        row_column_pairs[key] = value

# Convert dictionaries to dataframes
column_row_df = pd.DataFrame(list(column_row_pairs.items()), columns=["Key", "Value"])
row_column_df = pd.DataFrame(list(row_column_pairs.items()), columns=["Key", "Value"])

# Append the two dataframes
appended_df = column_row_df._append(row_column_df, ignore_index=True)

# Order the dataframe by the first digit of the key
appended_df["First Digit"] = appended_df["Key"].str.split("-").str[0].astype(int)
appended_df = appended_df.sort_values(by="First Digit").drop(columns=["First Digit"])

# Write the appended dataframe to a CSV file
appended_df.to_csv("appended_seedrecords.csv", index=False)
