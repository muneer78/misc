import re


def extract_reddit_names(input_file, output_file):
    # Read the input file
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Extract strings after 'r/' and between plus signs
    reddit_names = []
    for line in lines:
        matches = re.findall(r"\+(\w+)", line)
        reddit_names.extend(matches)

    # Write the extracted names to the output file
    with open(output_file, "w") as f:
        for name in reddit_names:
            f.write(name + "\n")


# Define input and output file paths
input_file = "/Users/muneer78/Downloads/docs/subs-3.txt"  # Replace with the actual path to your input file
output_file = "/Users/muneer78/Downloads/reddit_names-2.txt"

# Call the function to extract names and write to the output file
extract_reddit_names(input_file, output_file)

print(f"Reddit names have been written to {output_file}.")
