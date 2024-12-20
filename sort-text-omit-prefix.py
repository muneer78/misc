import re

# File path to your .md file
file_path = "/Users/muneer78/Documents/Projects/books.md"

# Function to remove "The " from the start of a title for sorting purposes
def sort_key(line):
    match = re.match(r"\| (.*?) \|", line)
    if match:
        title = match.group(1).lower()
        return title.removeprefix("the ")
    return line.lower()

# Read and process the .md file
with open(file_path, "r") as file:
    lines = file.readlines()

# Separate header, divider, and data
header = lines[0]
divider = lines[1]
data = lines[2:]

# Sort the data by title
sorted_data = sorted(data, key=sort_key)

# Write the sorted content back to the file
with open(file_path, "w") as file:
    file.write(header)
    file.write(divider)
    file.writelines(sorted_data)

print("Data has been sorted and saved!")
