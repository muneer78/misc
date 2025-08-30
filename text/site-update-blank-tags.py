# import os
#
# # Set the directory to the path where your Markdown files are located
# directory = '/Users/muneer78/Desktop/saved/'  # Replace this with the actual path
#
# # Iterate through all files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith('.md'):
#         filepath = os.path.join(directory, filename)
#
#         # Read the content of the file
#         with open(filepath, 'r') as file:
#             lines = file.readlines()
#
#         # Modify lines that only contain "tags:"
#         modified_lines = [
#             line if line.strip() != "title: Great Lines" else "title: "
#             for line in lines
#         ]
#
#         # Write the modified content back to the file
#         with open(filepath, 'w') as file:
#             file.writelines(modified_lines)
#
# print("Completed processing all Markdown files.")

import os

# Set the directory to the path where your Markdown files are located
directory = "/Users/muneer78/quartz/content/"  # Replace this with the actual path

# Iterate through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".md"):
        filepath = os.path.join(directory, filename)

        # Read the content of the file
        with open(filepath, "r") as file:
            lines = file.readlines()

        # Modify lines that contain "title: Great Lines"
        modified_lines = [
            line.replace("title: Great Lines", "title:").strip() + "\n"
            if "title: Great Lines" in line
            else line
            for line in lines
        ]

        # Write the modified content back to the file
        with open(filepath, "w") as file:
            file.writelines(modified_lines)

print("Completed processing all Markdown files.")
