import json

# Filepath to the JSON file
input_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\get_regions.json"
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\get_regions_sorted.json"

# Read the JSON file
with open(input_file, "r") as file:
    data = json.load(file)

# Sort the region_states dictionary by keys
data["region_states"] = dict(sorted(data["region_states"].items()))

# Write the updated JSON back to a file with proper formatting
with open(output_file, "w") as file:
    json.dump(data, file, indent=2)

print(f"Sorted JSON written to {output_file}")
