import subprocess

# Input list of strings with line breaks
input_string = """4532163
4303118
3502786
2827079
4352662
4126979
1327781
4988752
4970411
4694608
"""


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


# Split the input into a list of strings without quotes around each item
strings_list = input_string.strip().split("\n")
result = ", ".join(strings_list)

# Enclose the result in parentheses
final_result = f"in ({result})"

# Print paren enclosed result to the terminal
print(final_result)

# Copy paren enclosed result to the clipboard
copy2clip(final_result)
