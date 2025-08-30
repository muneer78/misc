import pandas as pd

# Read the v2 file (target for update)
df_v2 = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\password-rotation-source-v2.csv"
)
# Read the source file (provides Rotation Deadline)
df_src = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\password-rotation-source.csv"
)

# Merge Rotation Deadline into v2 using PasswordID as key
df_v2 = df_v2.merge(
    df_src[["PasswordID", "Rotation Deadline"]], on="PasswordID", how="left"
)

# Update the 'Current Deadline' column in v2 with the value from 'Rotation Deadline'
df_v2["Current Deadline"] = df_v2["Rotation Deadline"]

# Drop the extra 'Rotation Deadline' column (optional)
df_v2 = df_v2.drop(columns=["Rotation Deadline"])

# Save the updated v2 file
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\password-rotation-source-v2-updated.csv"
df_v2.to_csv(output_file, index=False)
print(f"Updated file written to {output_file}")

# Save the updated v2 file to a new CSV file
output_csv = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\password-rotation-source-v2-joined.csv"
df_v2.to_csv(output_csv, index=False)
print(f"Joined file written to {output_csv}")
