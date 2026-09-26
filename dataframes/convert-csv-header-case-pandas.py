import pandas as pd
import re

# Read the CSV file
input_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\pws-access-users.csv"
output_file = (
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\pws-access-users-modified.csv"
)

df = pd.read_csv(input_file)


# Function to convert headers
def convert_header(header):
    # Convert to lowercase
    header = header.lower()
    # Replace spaces with dashes
    header = header.replace(" ", "-")
    # Insert dashes between camel case characters
    header = re.sub(r"(?<!^)(?=[A-Z])", "-", header)
    return header


# Apply the function to all headers
df.columns = [convert_header(col) for col in df.columns]

# Write the modified CSV to a new file
df.to_csv(output_file, index=False)

print(f"Modified CSV written to {output_file}")
