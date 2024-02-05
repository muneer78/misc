# Input list of strings with line breaks
input_string = """Armen Budagov
Ashli Hill
Blake Levine
Colton Donahue
Enrique Andrade
Eric Berner
Gonzalo Faggioni
Jerren Dexter
Landon Kittle
Matt Bernard
Nagi Williams
Nick Rich
Seth Holman
Seth Sinnett
Sheen Lowery
Simeon Daskalov
Taylor Godberson
"""

# Split the input into a list of strings
strings_list = input_string.strip().split("\n")

# Separate each string with a comma
result = ", ".join(strings_list)

# Print the result to the terminal
print(result)
