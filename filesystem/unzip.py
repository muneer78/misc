import pyzipper

password = "green"

with pyzipper.AESZipFile(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\results-2025-May-14-121737.zip",
    "r",
    compression=pyzipper.ZIP_DEFLATED,
    encryption=pyzipper.WZ_AES,
) as extracted_zip:
    extracted_zip.extractall(pwd=str.encode(password))
