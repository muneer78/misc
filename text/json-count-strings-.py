import re


def use_regex(input_text):
    pattern = re.compile(r"\{(.+),", re.IGNORECASE)
    match = pattern.match(input_text)
    if match:
        return match.group(1)
    else:
        return None


text = '{"error":"DUPLICATES_DETECTED","fields":'
output = use_regex(text)

print(output)
