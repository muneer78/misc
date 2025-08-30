import pandas as pd

# Read the CSV file
input_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\pws-access-pwd-v2.csv"
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\pws-access-pwd-final.csv"

df = pd.read_csv(input_file)

# Add a new column called 'access-type'
df["access-type"] = df.apply(
    lambda row: "guest"
    if row["guest"] == "Yes"
    else "modify"
    if row["modify"] == "Yes"
    else "view"
    if row["view"] == "Yes"
    else "admin"
    if row["admin"] == "Yes"
    else "",
    axis=1,
)

# Drop the 'guest', 'modify', 'admin', and 'view' columns
df.drop(columns=["guest", "modify", "admin", "view"], inplace=True)

# Write the modified CSV to a new file
df.to_csv(output_file, index=False)

print(f"Modified CSV written to {output_file}")
