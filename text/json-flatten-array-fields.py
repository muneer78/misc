import pandas as pd
import json

# Load the CSV file
file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\Parameters_20250221.csv"
df = pd.read_csv(file_path)


# Function to recursively flatten nested JSON fields
def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


# Function to extract nested arrays and add them as new fields
def extract_nested_arrays(row, field_name):
    try:
        # Check if the field value is a string
        if isinstance(row[field_name], str):
            # Replace single quotes with double quotes
            data = json.loads(row[field_name].replace("'", '"'))
            flattened_data = flatten_json(data)
            for key, value in flattened_data.items():
                row[f"{field_name}_{key}"] = value
    except (json.JSONDecodeError, TypeError):
        pass
    return row


# Apply the function to extract nested arrays in specific fields
df = df.apply(lambda row: extract_nested_arrays(row, "pickup"), axis=1)
df = df.apply(lambda row: extract_nested_arrays(row, "delivery"), axis=1)
df = df.apply(lambda row: extract_nested_arrays(row, "extra_report_fields"), axis=1)

# Calculate the minimum and maximum number of fields a single record contains
min_fields = df.apply(lambda row: row.count(), axis=1).min()
max_fields = df.apply(lambda row: row.count(), axis=1).max()

# Write the updated DataFrame to a new CSV file
output_file = (
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\hubtek_exceptions_extracted.csv"
)
df.to_csv(output_file, index=False)

print(f"Updated CSV written to {output_file}")
print(f"Minimum number of fields in a single record: {min_fields}")
print(f"Maximum number of fields in a single record: {max_fields}")
