import pandas as pd

# Set file_name
file_name = "file.csv"

# # Use if reading CSV file
df = pd.read_csv(file_name)

# Use if reading Excel file
df = pd.read_excel(file_name)

# Drop rows where 'carrier_authority_date' is blank or null
df = df.dropna(subset=["carrier_authority_date"])

# Trim whitespace
df["carrier_authority_date"] = df["carrier_authority_date"].str.strip()
df["opp_id"] = df["opp_id"].str.strip()
df["status"] = df["status"].str.strip()

# Select specific columns
df = df[["opp_id", "status", "carrier_authority_date"]]

# Create df1
df1 = df[df["status"] == "Open"]

# Create df2
df2 = df[df["status"] == "Won"]

# Drop the 'status' column from both dataframes
df1 = df1.drop(columns=["status"])
df2 = df2.drop(columns=["status"])

# Write dataframes to CSV files
df1.to_csv("df1.csv", index=False)
df2.to_csv("df2.csv", index=False)

print("All done")
