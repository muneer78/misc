from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when

# Initialize Spark session
spark = SparkSession.builder.appName("RS Migration Classify").getOrCreate()

# Load the Excel file using the com.crealytics.spark.excel package
df = (
    spark.read.format("com.crealytics.spark.excel")
    .option("header", "true")
    .option("inferSchema", "true")
    .option("sheetName", "Sheet1")
    .load(
        "C:\\Users\\mahmad\\OneDrive - Ryan RTS\\projects\\rs-migration-classify.xlsx"
    )
)

# Ensure the columns are of string type before comparison
df = df.select(
    col("db_name").cast("string"),
    col("schema_name").cast("string"),
    col("table_name").cast("string"),
    *[col(c) for c in df.columns if c not in ["db_name", "schema_name", "table_name"]],
)

# Initialize the columns to "N/A"
df = (
    df.withColumn("Business_Unit", lit("N/A"))
    .withColumn("Data_Source", lit("N/A"))
    .withColumn("Derived_or_Direct", lit("N/A"))
)

# Define conditions and corresponding values
conditions = [
    (
        (col("db_name") == "CADNCEPRD")
        | (col("schema_name").isin(["cadence", "cadncedm"]))
        | (col("table_name") == "rpl_cadence_details__c"),
        {
            "Business_Unit": "Factoring",
            "Data_Source": "Factorsoft",
            "Derived_or_Direct": "Direct",
        },
    ),
    (
        col("table_name").rlike("(?i)factor"),  # Case-insensitive regex for "factor"
        {
            "Business_Unit": "Factoring",
            "Data_Source": "Factorsoft",
            "Derived_or_Direct": "Derived",
        },
    ),
]

# Apply the conditional updates
for condition, values in conditions:
    df = (
        df.withColumn(
            "Business_Unit",
            when(condition, lit(values["Business_Unit"])).otherwise(
                col("Business_Unit")
            ),
        )
        .withColumn(
            "Data_Source",
            when(condition, lit(values["Data_Source"])).otherwise(col("Data_Source")),
        )
        .withColumn(
            "Derived_or_Direct",
            when(condition, lit(values["Derived_or_Direct"])).otherwise(
                col("Derived_or_Direct")
            ),
        )
    )

# Create df of all updates
updates_only = df.filter(col("Business_Unit") != "N/A")

# Clear cells where value is "N/A"
df = (
    df.withColumn(
        "Business_Unit",
        when(col("Business_Unit") == "N/A", lit(None)).otherwise(col("Business_Unit")),
    )
    .withColumn(
        "Data_Source",
        when(col("Data_Source") == "N/A", lit(None)).otherwise(col("Data_Source")),
    )
    .withColumn(
        "Derived_or_Direct",
        when(col("Derived_or_Direct") == "N/A", lit(None)).otherwise(
            col("Derived_or_Direct")
        ),
    )
)

# Write the updated DataFrame to an Excel file
df.write.format("com.crealytics.spark.excel").option("header", "true").save(
    "C:\\Users\\mahmad\\OneDrive - Ryan RTS\\projects\\rs-migration-classify-test.xlsx"
)

# Define columns to save for updates only
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

# Select and write updates to CSV
updates_list = updates_only.select(columns)
updates_list.write.csv("rs-updates.csv", header=True)
