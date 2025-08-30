import polars as pl

# Read the Excel file
df1 = pl.read_excel(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\projects\rpl_lead-20241220-Redshift_Prod.xlsx",
    sheet_name="rpl_lead-20241220-Redshift_Prod",
)

# Apply the formula logic to filter the DataFrame
df = df1.filter(pl.col("diff?") == "true")

# Print the filtered DataFrame
print(df)

# Save the updated DataFrame back to a CSV file
df.write_csv("5577_lead_final.csv")
