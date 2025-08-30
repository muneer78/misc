import pandas as pd


def load_and_sort_csv(file_name):
    df = pd.read_csv(file_name)
    df_sorted = df.sort_values(by=["Account"])
    return df_sorted


def find_diff_rows(df1, df2, column_name):
    comparison_result = df1[column_name].ne(df2[column_name])
    return df1[comparison_result]


# Load and sort leads data
df_old = load_and_sort_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\20250204_salesforce_responses.csv"
)
df_new = load_and_sort_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\20250205_salesforce_responses.csv"
)

# Find rows with differences in the Account column
diff = find_diff_rows(df_old, df_new, "Account")

# Count the number of rows with differences
print(f"Number of rows in {df_old}", len(df_old))
print(f"Number of rows in {df_old}", len(df_new))

diff_count = len(diff)
print(f"Number of rows with differences in the 'Account' column: {diff_count}")
