import subprocess

# Input list of strings with line breaks
input_string = """ZIB01USD
ZIB01USD
Z8131325
Z8131325
XFER    
XFER    
WT080912
WT080912
WT080612
WT080612
WT080612
WT080612
WT050212
WT050212
WMS     
WMS     
WL438449
WL438449
WIRE PRE
WIRE PRE
WIRE PRE
WIRE PRE
WIRE PRE
WIRE9102
WIRE9102
WIRE8.31
WIRE8.31
WIRE8152
WIRE8152
WIRE4262
WIRE4262
WIRE4222
WIRE4222
WIRE4132
WIRE4132
WIRE3422
WIRE3422
WIRE3132
WIRE3132
WIRE3112
WIRE3112
WIRE2.6.
WIRE2.6.
WIRE2112
WIRE2112
WIRE1722
WIRE1722
WIRE1230
WIRE1230
WIRE1229
WIRE1229
WIRE1229
WIRE1229
WIRE1223
WIRE1223
WIRE1223
WIRE1223
WIRE1222
WIRE1222
WIRE1216
WIRE1216
WIRE1216
WIRE1216
WIRE1215
WIRE1215
WIRE1214
WIRE1214
WIRE1213
WIRE1213
"""

# Remove duplicates and preserve order
unique_strings = list(
    dict.fromkeys(line.strip() for line in input_string.strip().splitlines())
)

# Format the list as a comma-separated string with single quotes
formatted_list = [f"'{item}'" for item in unique_strings]
result = ", ".join(formatted_list)


# Function to copy to clipboard
def copy2clip(txt):
    cmd = "echo " + txt.strip() + "| clip"
    return subprocess.check_call(cmd, shell=True)


# Copy the formatted string to the clipboard
copy2clip(result)
