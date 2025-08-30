import csv


def csv_to_dict(file_path, col_name_key, data_type_key):
    """
    Reads a CSV file and converts it to a list of dictionaries,
    extracting only specified keys for each row.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [
            {
                col_name_key: row.get(col_name_key, "").strip(),
                data_type_key: row.get(data_type_key, "").strip(),
            }
            for row in reader
        ]


# Transformation rules
type_mapping = {
    "text": "string",
    "smallint": "int",
    "bigint": "int",
    "integer": "int",
    "double precision": "double",
    "numeric": "double",
    "timestamp without time zone": "timestamp",
    "datetime": "timestamp",
    "nvarchar": "string",
    "varchar": "string",
    "character varying": "string",
    "nvarchar": "string",
    "bit": "boolean",
    "money": "double",
    "decimal": "double",
}


def apply_type_mapping(fields, type_mapping):
    """
    Updates the data types in a list of field dictionaries based on a given type mapping.
    """
    return [
        {
            "column_name": field["column_name"].strip().lower(),
            "data_type": type_mapping.get(
                field["data_type"].strip().lower(), field["data_type"].strip().lower()
            ),
        }
        for field in fields
    ]


def list_to_dict(fields):
    """
    Converts a list of dictionaries to a dictionary with column_name as the key
    and data_type as the value. Keys are converted to lowercase and sorted alphabetically.
    """
    return {
        field["column_name"].strip().lower(): field["data_type"].strip().lower()
        for field in sorted(fields, key=lambda x: x["column_name"].strip().lower())
    }


def compare_fields(name1, name2, dict1, dict2):
    """
    Compares two dictionaries for missing keys and mismatched data types.
    Returns the comparison results as a dictionary.
    """
    missing_in_dict2 = set(dict1.keys()) - set(dict2.keys())
    missing_in_dict1 = set(dict2.keys()) - set(dict1.keys())
    type_mismatches = {
        key: (dict1[key], dict2[key])
        for key in dict1
        if key in dict2 and dict1[key] != dict2[key]
    }
    return {
        "missing_in_dict2": missing_in_dict2,
        "missing_in_dict1": missing_in_dict1,
        "type_mismatches": type_mismatches,
    }


def process_comparisons(output_file="comparison_results.md", **kwargs):
    """
    Accepts 3 or 4 dictionaries and compares them pairwise.
    Saves the comparison results to a Markdown file.
    """
    keys = list(kwargs.keys())
    num_dicts = len(keys)

    if num_dicts not in [3, 4]:
        raise ValueError("The function accepts exactly 3 or 4 dictionaries.")

    output_lines = []

    # Compare each pair of dictionaries
    for i in range(num_dicts):
        for j in range(i + 1, num_dicts):
            name1, dict1 = keys[i], kwargs[keys[i]]
            name2, dict2 = keys[j], kwargs[keys[j]]
            result = compare_fields(name1, name2, dict1, dict2)

            # Format the comparison results
            output_lines.append(f"## Comparison: {name1} vs {name2}\n")
            output_lines.append(f"### Keys in {name1} that are not in {name2}:\n")
            output_lines.extend(
                f"- {key}" for key in sorted(result["missing_in_dict2"])
            )
            if not result["missing_in_dict2"]:
                output_lines.append("No mismatches found.")

            output_lines.append(f"\n### Keys in {name2} that are not in {name1}:\n")
            output_lines.extend(
                f"- {key}" for key in sorted(result["missing_in_dict1"])
            )
            if not result["missing_in_dict1"]:
                output_lines.append("No mismatches found.")

            output_lines.append("\n### Keys with mismatched types:\n")
            output_lines.extend(
                f"- {key}: {name1}={types[0]}, {name2}={types[1]}"
                for key, types in sorted(result["type_mismatches"].items())
            )
            if not result["type_mismatches"]:
                output_lines.append("No mismatches found.")
            output_lines.append("\n" + "=" * 50 + "\n")

    # Write to file
    with open(output_file, "w") as file:
        file.write("\n".join(output_lines))


# Example usage
file_dbx = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\debtors.csv"
file_rs = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\svv_columns-20241121.csv"
file_pg = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\columns-20241121.csv"
file_cadence = (
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\COLUMNS-20241121-1732207220098.csv"
)

# Load and preprocess data
dbx_fields = csv_to_dict(file_dbx, "col_name", "data_type")
for field in dbx_fields:
    field["column_name"] = field.pop("col_name")
redshift_fields = csv_to_dict(file_rs, "column_name", "data_type")
pg_fields = csv_to_dict(file_pg, "column_name", "data_type")
cadence_fields = csv_to_dict(file_cadence, "column_name", "data_type")

# Apply type mappings
dbx_dict = list_to_dict(apply_type_mapping(dbx_fields, type_mapping))
redshift_dict = list_to_dict(apply_type_mapping(redshift_fields, type_mapping))
pg_dict = list_to_dict(apply_type_mapping(pg_fields, type_mapping))
cadence_dict = list_to_dict(apply_type_mapping(cadence_fields, type_mapping))

# Call process_comparisons with 3 or 4 dictionaries
process_comparisons(
    output_file="comparison_results.md",
    dbx=dbx_dict,
    redshift=redshift_dict,
    postgres=pg_dict,
    cadence=cadence_dict,
)
