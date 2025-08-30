# Define the input and output file names
input_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\projects\powerbi-dataset-ids.txt"  # replace with your input file name
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\projects\powerbi-dataset-strings.txt"  # replace with your desired output file name

# Open the input file for reading
with open(input_file, "r") as file:
    # Replace commas and whitespace with underscores and append '.bim'
    lines = [line.replace(",", "_").replace(" ", "_") for line in file]


# Open the output file for writing
with open(output_file, "w") as file:
    # Write the modified lines to the output file
    file.writelines(lines)

print(f"Replaced commas with underscores in {input_file} and saved to {output_file}.")
