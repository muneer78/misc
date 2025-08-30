import pandas as pd

# Define the path to the CSV file
csv_file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\Book1.csv"

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Extract values after 'ocr/' on each line from the source_file_name column
extracted_values = (
    df["error_message"]
    .apply(lambda x: x.split(": ")[1] if ": " in x else None)
    .dropna()
)

# Dedupe values and only provide the unique values
unique_values = sorted(set(extracted_values))

# Convert the list of unique values to a DataFrame
unique_values_df = pd.DataFrame(unique_values, columns=["unique_values"])

# Save the unique values to a CSV file
unique_values_df.to_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\unique_values.csv", index=False
)

print("Unique values saved to unique_values.csv")
