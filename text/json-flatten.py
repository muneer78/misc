import pandas as pd
import json

# Load the CSV file
file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\brok_hubtek_quote_parameter_v9-20250214-Redshift_Prod.csv"
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
        data = json.loads(row[field_name])
        flattened_data = flatten_json(data)
        for key, value in flattened_data.items():
            row[f"{field_name}_{key}"] = value
    except (json.JSONDecodeError, TypeError):
        pass
    return row


# Apply the function to extract nested arrays in Hubtek fields
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'additional_data'), axis=1)

# Apply the function to extract nested arrays in DBX fields
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.seasonality'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.distance_tiers.distance_tiers'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.lead_time.times'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.rate_engines_weight.engines'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.conditioned_lanes.origins'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.conditioned_lanes.destinations'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.cross_border.lanes'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.international_shipment.lanes'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'parameters.extra_charges_and_restrictions.extra_charges_and_restrictions'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'additional_data.equipment_type_keywords.0'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'additional_data.equipment_type_keywords.1'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'additional_data.equipment_type_keywords.2'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'additional_data.equipment_type_keywords.3'), axis=1)
# df = df.apply(lambda row: extract_nested_arrays(row, 'additional_data.equipment_type_keywords.4'), axis=1)

# Apply the function to extract nested arrays in Redshift fields
df = df.apply(lambda row: extract_nested_arrays(row, "parameters_pickuptm"), axis=1)
df = df.apply(
    lambda row: extract_nested_arrays(row, "parameters_transittimevariance"), axis=1
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "parameters_distancetiersdistancetiers"),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "parameters_leadtimetimes"), axis=1
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "parameters_rateenginesweightengines"),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "parameters_crossborderlanes"), axis=1
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "parameters_internationalshipmentlanes"),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(
        row, "parameters_extrachargesandrestrictionsextrachargesandrestrictions"
    ),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "additionaldata_emailnotificationemails"),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "additional_data.equipmenttypekeywords0"),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "additional_data.equipmenttypekeywords1"),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "additional_data.equipmenttypekeywords2"),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "additional_data.equipmenttypekeywords3"),
    axis=1,
)
df = df.apply(
    lambda row: extract_nested_arrays(row, "additional_data.equipmenttypekeywords.4"),
    axis=1,
)

# Calculate the minimum and maximum number of fields a single record contains
min_fields = df.apply(lambda row: row.count(), axis=1).min()
max_fields = df.apply(lambda row: row.count(), axis=1).max()

# Write the updated DataFrame to a new CSV file
output_file = (
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\dbx_parameters_extracted.csv"
)
df.to_csv(output_file, index=False)

print(f"Updated CSV written to {output_file}")
print(f"Minimum number of fields in a single record: {min_fields}")
print(f"Maximum number of fields in a single record: {max_fields}")
