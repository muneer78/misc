# import pandas as pd

# # Load the CSV file
# file = (
#     r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\RtsTransactionsFtp2024-10-04.csv"
# )
# # file2 = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\RtsTransactionsFtp2024-10-05.csv"

# df = pd.read_csv(file)

# # Function to find the most common value in each column
# def find_common_patterns(df):
#     common_patterns = {}
#     for column in df.columns:
#         common_patterns[column] = df[column].mode()
#     return common_patterns

# # Find common patterns in the file
# patterns = find_common_patterns(df)

# # Identify rows where the pattern is not matched
# mismatched_rows = df.copy()
# for column, pattern in patterns.items():
#     mismatched_rows = mismatched_rows[mismatched_rows[column] != pattern]

# # Write mismatched rows to an output CSV file
# output_file = "mismatched_rows.csv"
# mismatched_rows.to_csv(output_file, index=False)

# # Display the common patterns and a message about the output file
# print("Most common patterns in each column:")
# for column, pattern in patterns.items():
#     print(f"Column: {column}, Most Common Value: {pattern}")

# print(f"\nRows where the pattern is not matched have been written to {output_file}")

import pandas as pd
import data_patterns

# Load the CSV file
file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\RtsTransactionsFtp2024-10-04.csv"
df = pd.read_csv(file)

# setting datag=frame index
df.set_index("BillingServiceAccountNo", inplace=True)

# creating a pattern mixer object
miner = data_patterns.PatternMiner(df)


# finding the pattern in the dataframe
# name is optional
# other patterns which can be used  ‘>’, ‘<’, ‘<=’, ‘>=’, ‘!=’, ‘sum’
df_patterns = miner.find(
    {
        "name": "equal values",
        "pattern": "=",
        "parameters": {"min_confidence": 0.5, "min_support": 2, "decimal": 8},
    }
)


# getting the analyzed dataframe
df_results = miner.analyze(df)


# printing the analyzed results
print(df_results)
