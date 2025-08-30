import subprocess


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


# Given list of items
items = """
nk_sfacctid, nk_sfacctid, rtsf_customer_status_c, rtsf_customer_status_c, main_rtscs_customer_status__c, rtscs_customer_status__c, rtsi_customer_status__c, rtsi_customer_status__c
"""

# Split the items by comma and newline and strip any extra whitespace
item_list = [item.strip() for item in items.replace("\n", "").split(",")]

# Get unique items by converting the list to a set and then back to a list to maintain order
unique_items = list(set(item_list))

unique_items.sort()

# Join the items with a newline character
formatted_items = "\n".join(unique_items)

# Print the formatted items to verify the output
print(formatted_items)

# Copy to the clipboard
copy2clip(formatted_items)
