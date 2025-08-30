import subprocess

# Input list of strings with line breaks
input_string = """ZORADAIL
ZORABRIL
ZOOTLANV
ZOOSGRCO
ZOOMTOT1
ZOOMQUNY
ZOOMMETX
ZOOMGRWI
ZOOMANIN
ZOOKBHPA
ZOODJUCA
"""

# Split the input into a list of strings with single quotes around each item, preserving whitespace
strings_list = input_string.split("\n")
formatted_list = [f"'{name}'" for name in strings_list if name.strip()]
result = ", ".join(formatted_list)


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "| clip"
    return subprocess.check_call(cmd, shell=True)


print(result)
# Copy the formatted string to the clipboard
copy2clip(result)
