import base64

base64_string = "cHJhdGVzLVljNTVwNmJ1WjdEV2J3Zkc="
base64_bytes = base64_string.encode("utf-8")

string_bytes = base64.b64decode(base64_bytes)
string = string_bytes.decode("utf-8")

print(f"Decoded string: {string}")  # Out
