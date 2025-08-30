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

# Find common fields
common_fields = sorted(rs_set.intersection(dbx_set))

# Find fields in dbx but not in rs
dbx_not_in_rs = sorted(dbx_set.difference(rs_set))

# Find fields in rs but not in dbx
rs_not_in_dbx = sorted(rs_set.difference(dbx_set))

# Write the results to a new file
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\comparison_results.txt"
with open(output_file, "w") as file:
    file.write("Common fields:\n")
    file.write("\n".join(common_fields))
    file.write("\n\nFields in dbx but not in rs:\n")
    file.write("\n".join(dbx_not_in_rs))
    file.write("\n\nFields in rs but not in dbx:\n")
    file.write("\n".join(rs_not_in_dbx))

print(f"Comparison results written to {output_file}")
