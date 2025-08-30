import difflib

# Read the contents of the files
with open(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\rs-parameters.txt", "r"
) as file:
    rs_parameters = file.read().splitlines()

with open(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\dbx-parameters.txt", "r"
) as file:
    dbx_parameters = file.read().splitlines()

# Convert the lists to sets for comparison
rs_set = set(rs_parameters)
dbx_set = set(dbx_parameters)


# Function to determine if two fields match with at least 80% similarity
def is_match(field1, field2, threshold=0.8):
    return difflib.SequenceMatcher(None, field1, field2).ratio() >= threshold


# Find common fields with at least 80% similarity
common_fields = sorted({rs for rs in rs_set for dbx in dbx_set if is_match(rs, dbx)})

# Find fields in dbx but not in rs
dbx_not_in_rs = sorted(
    {dbx for dbx in dbx_set if not any(is_match(dbx, rs) for rs in rs_set)}
)

# Find fields in rs but not in dbx
rs_not_in_dbx = sorted(
    {rs for rs in rs_set if not any(is_match(rs, dbx) for dbx in dbx_set)}
)

# Write the results to a new file
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\comparison_results.txt"
with open(output_file, "w") as file:
    file.write("Common fields (80% similarity):\n")
    file.write("\n".join(common_fields))
    file.write("\n\nFields in dbx but not in rs:\n")
    file.write("\n".join(dbx_not_in_rs))
    file.write("\n\nFields in rs but not in dbx:\n")
    file.write("\n".join(rs_not_in_dbx))

print(f"Comparison results written to {output_file}")
