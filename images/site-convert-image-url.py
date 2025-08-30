import re
import subprocess


def copy2clip(txt):
    cmd = f'echo "{txt.strip()}" | pbcopy'
    return subprocess.check_call(cmd, shell=True)


# Define the old and new patterns
old_pattern = (
    r"!\[(.*?)\]\((https://buttondown-attachments\.s3\.amazonaws\.com/images/.*?)\)"
)
new_pattern_template = r"![\1](https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/\1.png)"


# Function to replace the old pattern with the new pattern
def replace_image_links(text):
    return re.sub(old_pattern, new_pattern_template, text)


# Example usage
old_text = "![livingwage.jpeg](https://buttondown-attachments.s3.amazonaws.com/images/d274f5a7-7dba-4aad-b38e-7299fdc61f75.jpeg)"
new_text = replace_image_links(old_text)

# Copy the new text to clipboard
copy2clip(new_text)

print("The updated image link has been copied to your clipboard.")
