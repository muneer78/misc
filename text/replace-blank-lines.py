# Read the content of the file
with open("mcleod.md", "r") as file:
    file_content = file.readlines()

# Filter out blank lines
filtered_content = [line for line in file_content if line.strip()]

# Write the filtered content back to the file
with open("mcleod.md", "w") as file:
    file.writelines(filtered_content)

# Count the number of rows
row_count = len(filtered_content)

# Calculate the midpoint of the list
midpoint = row_count // 2

# Return the content at the midpoint
midpoint_content = filtered_content[midpoint] if row_count > 0 else None
print(f"Midpoint content: {midpoint_content}")
