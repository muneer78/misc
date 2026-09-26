import pandas as pd

# Read the Excel file
df = pd.read_excel("Day 91 Load Stats.xlsx")

# Convert 'Date' column to datetime format
df["Date"] = pd.to_datetime(df["Date"])

# Format the 'Date' column
df["Date"] = df["Date"].dt.strftime("%m-%d-%Y")

# Calculate success rate
df["Success Rate"] = df["Successful Records"] / (
    df["Successful Records"] + df["Errored Records"]
)

# Format success rate as percentage
df["Success Rate"] = pd.Series(
    ["{0:.1f}%".format(val * 100) for val in df["Success Rate"]], index=df.index
)

# Write back to the Excel file
df.to_excel("Day 91 Load Stats.xlsx", index=False)
