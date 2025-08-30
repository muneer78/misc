import subprocess

# Input list of strings with line breaks
input_string = """58dd1c4dcbf83b0016aea2b2
58dd2c45cbf83b0016aea2b5
58dd353bcbf83b0016aea2b6
58de82d552869d00182251ac
58e56725a7279f00149de0c0
58eb9a4fc7904400142359e2
58ed51a6a6131c000d9bcf42
5916262ae56f51000cfe944b
5919ea4ce56f51000cfe944c
59440adfdbf074000c4de149
"""


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


# Split the input into a list of strings with quotes around each item
strings_list = input_string.strip().split("\n")
formatted_list = [f"'{name}'" for name in strings_list]
result = ", ".join(formatted_list)

# Enclose the result in parentheses
final_result = f"in ({result})"

# Print paren enclosed result to the terminal
print(final_result)

# Copy paren enclosed result to the clipboard
copy2clip(final_result)
