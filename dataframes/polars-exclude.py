import polars as pl

# DS4596

# Read the dataset from a CSV file
df1 = pl.read_csv("LeadErrors.csv")

# Define the error messages to filter out
error_messages = [
    "Please enter the Competitor to which this lead was lost.",
    "All Leads must contain at least one form of contact information. Please enter either a phone number or an email address.",
]

# Filter the DataFrame to exclude rows with the specified error messages
df1_updated = df1.filter(~(pl.col("ERROR").is_in(error_messages)))
df1_updated = df1_updated.drop(["ERROR"])

# Save the updated DataFrame back to a CSV file
df1_updated.write_csv("leadreloadupdated.csv")
