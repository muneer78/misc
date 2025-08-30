import subprocess
from rich import print


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


text_with_line_breaks = """AND(
OR(
$Profile.Name = 'RTSF Sales',
$Profile.Name = 'RTSF Sales Manager',
$Profile.Name = 'Continuous Improvement'
),
OR(
ISCHANGED(McLeod_Carrier_Id__c),
ISCHANGED(Name),
ISCHANGED(OwnerId)
)
)"""

# Remove spaces, line breaks, and carriage returns
text_without_line_breaks = (
    text_with_line_breaks.replace(" ", "").replace("\n", "").replace("\r", "")
)

print(text_without_line_breaks)

copy2clip(text_without_line_breaks)
