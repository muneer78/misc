from pathlib import Path
from datetime import datetime

# Specify the directory containing the files
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads")

# Dynamically generate the date string in YYYYMMDD format
date_str = datetime.now().strftime("%Y%m%d")

# Define a dictionary mapping old names to new names using f-strings
name_mapping = {
    f"COLUMNS-{date_str}.csv": f"sql-COLUMNS-{date_str}.csv",
    f"columns-{date_str}.csv": f"pg-columns-{date_str}.csv",
    f"svv_columns-{date_str}.csv": f"rs-svv_columns-{date_str}.csv",
}

# Iterate through the dictionary and rename files
for old_name, new_name in name_mapping.items():
    old_file = directory / old_name
    new_file = directory / new_name

    # Check if the old file exists before renaming
    if old_file.exists():
        old_file.rename(new_file)
        print(f"Renamed: {old_name} -> {new_name}")
    else:
        print(f"File {old_name} does not exist in the directory.")
