# Input list of strings with line breaks
input_string = """a
b
gc
d
e
g
h
i
"""

# Split the input into a list of strings
strings_list = input_string.strip().split("\n")

# Separate each string with a comma
result = ", ".join(strings_list)

# Print the result to the terminal
print(result)
