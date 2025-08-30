input_filename = "ask a manager.txt"
output_filename = "ask a manager-fixed.txt"

with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
    for line in input_file:
        if not line.startswith("► Expand"):
            output_file.write(line)

print("Lines starting with '► Expand' removed successfully.")
