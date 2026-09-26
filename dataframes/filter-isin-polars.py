import polars as pl

# Read the dataset from a CSV file
df = pl.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\part-00000-tid-7610326873113088696-a0955a82-98ed-4f0b-a957-b52de3c45f26-4-1-c000.csv"
)

# Convert the 'Class__c' column to uppercase and create a new column 'uppercase_Class__c'
df = df.with_columns(pl.col("Class__c").str.to_uppercase().alias("uppercase_Class__c"))

# Filter the records usins isin
# updated_df = df.filter(
#     pl.col("DOT_Number__c").is_in(
#         [
#             901149,
#             3551633,
#             3272608,
#             2084644,
#             1329510,
#             3934330,
#             3318509,
#             4107527,
#             3637719,
#             3414513,
#             2046380,
#             3486661,
#             3823018,
#             4089593,
#             1024009,
#             4029287,
#             728326,
#             3321304,
#             1444749,
#             3426030,
#             3305891,
#             4105507,
#             3694733,
#             3625008,
#             977831,
#             79127,
#             3424092,
#             4003610,
#             675236,
#             3027659,
#             2634486,
#             3220882,
#             3808871,
#             2967527,
#             4069255,
#             3274895,
#             3825460,
#             3978384,
#             3445904,
#             4101745,
#             2572955,
#             3404664,
#             1239587,
#             2537388,
#             3163128,
#             2558809,
#         ]
#     )
# )

# Filter the DataFrame where 'uppercase_Class__c' contains 'OTHER'
updated_df = df.filter(pl.col("uppercase_Class__c").str.contains("OTHER"))

# Columns to include in output
columns = [
    "FMCSA_Legal_Name__c",
    "DOT_Number__c",
    "Class__c",
    "Class_Other__c",
]

# Select the desired columns
final_df = updated_df.select(columns)

print(final_df)

df_sorted = final_df.sort(["FMCSA_Legal_Name__c"], descending=False)

# Write final file
df_sorted.write_csv("20240918carrierprofileoutput.csv")
