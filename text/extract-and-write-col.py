import pandas as pd
import re

# Define the path to the CSV file
csv_file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\kenpom25.csv"

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Extract any numbers from the 'Team' column and write to a new column called 'seed'
df["seed"] = df["Team"].apply(
    lambda x: re.search(r"\d+", str(x)).group() if re.search(r"\d+", str(x)) else None
)

# Remove numbers at the end of the 'Team' column before trimming whitespace
df["Team"] = df["Team"].str.replace(r"\d+$", "", regex=True).str.strip()


# Save the updated DataFrame to a new CSV file
output_file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\algo.csv"
df.to_csv(output_file_path, index=False)

print(f"Updated CSV with 'seed' column saved to {output_file_path}")
