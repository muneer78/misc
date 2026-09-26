import polars as pl

# Read the Excel file
df = pl.read_excel(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\projects\rs-migration-classify.xlsx",
    sheet_name="Sheet1",
)

# Ensure the columns are of string type before comparison
df = df.with_columns(
    [
        pl.col("db_name").cast(pl.Utf8),
        pl.col("schema_name").cast(pl.Utf8),
        pl.col("table_name").cast(pl.Utf8),
    ]
)

# Initialize the columns to "N/A"
df = df.with_columns(
    [
        pl.lit("N/A").alias("Business_Unit"),
        pl.lit("N/A").alias("Data_Source"),
        pl.lit("N/A").alias("Derived_or_Direct"),
    ]
)

# Define the update conditions and corresponding values
conditions = [
    (
        (pl.col("db_name") == "CADNCEPRD")
        | (pl.col("schema_name") == "cadence")
        | (pl.col("schema_name") == "cadncedm")
        | (pl.col("table_name") == "rpl_cadence_details__c"),
        {
            "Business_Unit": "Factoring",
            "Data_Source": "Factorsoft",
            "Derived_or_Direct": "Direct",
        },
    ),
    (
        (pl.col("table_name").str.contains("factor", literal=False)),
        {
            "Business_Unit": "Factoring",
            "Data_Source": "Factorsoft",
            "Derived_or_Direct": "Derived",
        },
    ),
]

# Apply the conditional updates
for condition, values in conditions:
    df = df.with_columns(
        [
            pl.when(condition)
            .then(pl.lit(values["Business_Unit"]))
            .otherwise(pl.col("Business_Unit"))
            .alias("Business_Unit"),
            pl.when(condition)
            .then(pl.lit(values["Data_Source"]))
            .otherwise(pl.col("Data_Source"))
            .alias("Data_Source"),
            pl.when(condition)
            .then(pl.lit(values["Derived_or_Direct"]))
            .otherwise(pl.col("Derived_or_Direct"))
            .alias("Derived_or_Direct"),
        ]
    )

# Create df of all updates
updates_only = df.filter(pl.col("Business_Unit") != "N/A")

# Clear all cells where value is "N/A" in Business_Unit, Data_Source, and Derived_or_Direct columns
df = df.with_columns(
    [
        pl.when(pl.col("Business_Unit") == "N/A")
        .then(pl.lit(None))
        .otherwise(pl.col("Business_Unit"))
        .alias("Business_Unit"),
        pl.when(pl.col("Data_Source") == "N/A")
        .then(pl.lit(None))
        .otherwise(pl.col("Data_Source"))
        .alias("Data_Source"),
        pl.when(pl.col("Derived_or_Direct") == "N/A")
        .then(pl.lit(None))
        .otherwise(pl.col("Derived_or_Direct"))
        .alias("Derived_or_Direct"),
    ]
)

# Write the updated DataFrame to an Excel file
df.write_excel(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\projects\rs-migration-classify-test.xlsx"
)

columns = [
    "Report ID",
    "workspace_id",
    "pbi_workspace_name",
    "dataset_name",
    "db_type",
    "db_name",
    "schema_name",
    "table_name",
    "Business_Unit",
    "Data_Source",
    "Derived_or_Direct",
]

updates_list = updates_only.select(columns)
updates_list.write_csv(r"rs-updates.csv")
