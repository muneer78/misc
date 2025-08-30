import subprocess


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


string = "SortandAddColumns"

newstring = string.lower()

print(newstring)

# Copy to the clipboard
copy2clip(newstring)
