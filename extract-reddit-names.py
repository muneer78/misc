def extract_lines(input_file, output_file):
    # Read the input file
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Filter lines that begin with 'r/' and have a single word
    filtered_lines = [
        line.strip()
        for line in lines
        if line.startswith("r/") and len(line.split()) == 1
    ]

    # Write the filtered lines to the output file
    with open(output_file, "w") as f:
        for line in filtered_lines:
            f.write(line + "\n")


# Define input and output file paths
input_file = "/Users/muneer78/Downloads/docs/subs.txt"  # Replace with the actual path to your input file
output_file = "/Users/muneer78/Downloads/filtered_lines.txt"

# Call the function to extract lines and write to the output file
extract_lines(input_file, output_file)

print(f"Filtered lines have been written to {output_file}.")
