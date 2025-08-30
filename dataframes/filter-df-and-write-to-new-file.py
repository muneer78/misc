import pandas as pd

# Read the dataset from a CSV file
df = pd.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\projects\pws-access-pwd.csv")

# Filter rows where notes column is 'Sara to review and recommend solution'
notes_filtered = df[df["notes"] == "Sara to review and recommend solution"]

# Filter rows where recommendation column is not null
recommendation_filtered = df[df["recommendation"].notnull()]

# Sort each set of records first by title column, and then by user-or-security-group column
notes_filtered_sorted = notes_filtered.sort_values(
    by=["title", "user-or-security-group"]
)
recommendation_filtered_sorted = recommendation_filtered.sort_values(
    by=["title", "user-or-security-group"]
)

# Concatenate the two sets of records
result = pd.concat([notes_filtered_sorted, recommendation_filtered_sorted])

# Write the filtered and sorted rows to a new CSV file
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\pws-action-items.csv"
result.to_csv(output_file, index=False)

print(f"Filtered and sorted CSV written to {output_file}")
