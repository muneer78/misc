import pandas as pd

# Read the dataset from a CSV file, ensuring all columns are read and empty values are handled
df = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\20250312-passwords.csv"
)

# Search the 'title' field for strings "API" or "FTP" and update the 'Must be on network' field to "1"
df.loc[
    df["Title"].str.contains("API|FTP", case=False, na=False), "Must be on network"
] = "1"

# Print the updated rows to the console
updated_rows = df[df["Title"].str.contains("API|FTP", case=False, na=False)]
print("\nUpdated Rows:")
print(updated_rows)

# Save the updated DataFrame back to a CSV file
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\password-update.csv"
df.to_csv(output_file, index=False)

print(f"Modified CSV written to {output_file}")
