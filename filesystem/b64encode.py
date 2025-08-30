import base64

string = "cHJhdGVzLVljNTVwNmJ1WjdEV2J3Zkc="
string_bytes = string.encode("utf-8")

base64_bytes = base64.b64encode(string_bytes)
base64_string = base64_bytes.decode("utf-8")

print(
    f"Encoded string: {base64_string}"
)  # Output: Decoded string: cypress-Yc55p6buW7DWbwfg
