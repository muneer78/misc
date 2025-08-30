import subprocess

# Input list of strings with line breaks
input_string = """15B9B3277C38460ABA2427B23C04FD6D
15E2C03378B9449DAD15CD426E6A2996
170F8AFB22794553A468E8B22455CF27
171364C007B84309BCD6954749BA75FB
171CF46E93EB4A59BD34BF2DEDADD3D0
17DF05B6DF2A473894EDADCAFF2ED99D
18010E92E9EE4BFDB120868D778F22CE
18212E0475DF490B827C103863B7012C
18381387CCA749BDB83F2B49733CD600
1842FFAECC9C4393948DF3225F9B6965
186CC7C95B4A4FFB8BFD46849D14DBD3
"""

# Trim the whitespace from each line and join with commas
trimmed_string = ",".join(line.strip() for line in input_string.strip().splitlines())

# Split the input into a list of strings with single quotes around each item
strings_list = input_string.strip().split("\n")
formatted_list = [f"'{name.strip()}'" for name in strings_list]
result = ", ".join(formatted_list)


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "| clip"
    return subprocess.check_call(cmd, shell=True)


print(result)
# Copy the formatted string to the clipboard
copy2clip(result)
# copy2clip(trimmed_string)
