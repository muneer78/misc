import polars as pl

# Set df column as list
# Read the CSV file into a DataFrame
df = pl.read_csv("DS4013_20240607134926_output.csv")

# Extract the "id" column as a list
strings_list = df["factorsoft_client_number__c"].to_list()

# # Split the pasted input into a list of strings
# # Split the input into a list of strings
# input_string = """0011H00001ncIHxQAM
# 0011H00001ncC4RQAU
# 0011H00001nbv7LQAQ
# 0011H00001nP2JbQAK
# 0011H00001nbu4sQAA
# 0011H00001nP27vQAC
# 0011H00001ncB4XQAU
# 0011H00001nP2ZRQA0"""
# strings_list = input_string.strip().split("\n")

# Create result
result = ", ".join(strings_list)

# Group strings into groups of 40
group_size = 40
groups = [
    strings_list[i : i + group_size] for i in range(0, len(strings_list), group_size)
]

# Split the list of files into groups of size 'group_size'
file_groups = [
    strings_list[i : i + group_size] for i in range(0, len(strings_list), group_size)
]

# Print each group to the console
for i, group in enumerate(groups):
    print(f"Group {i + 1}: {', '.join(group)}")
