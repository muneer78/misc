from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc
from datetime import datetime as dt

# Initialize Spark session
spark = SparkSession.builder.appName("DataFrameMerge").getOrCreate()

# Get the current date
current_date = dt.now()

# Read the CSV files
df1 = spark.read.csv(
    "C:/Users/mahmad/OneDrive - Ryan RTS/Code/powerbi-research-rework.csv",
    header=True,
    inferSchema=True,
)
df2 = spark.read.csv(
    "C:/Users/mahmad/OneDrive - Ryan RTS/Code/rs_unique.csv",
    header=True,
    inferSchema=True,
)

# Rename the column in df2 to match df1
df2 = df2.withColumnRenamed("dataset", "dataset_id")

# Perform the left join
result = df1.join(df2, on="dataset_id", how="left")

# Select all columns from df1 and specific columns from df2
selected_columns = df1.columns + ["isredshift"]
result = result.select(*selected_columns)

# Convert 'Last View Date' to datetime if needed (uncomment if this field is present and needs transformation)
# result = result.withColumn("Last View Date", to_date(col("Last View Date"), "MM/dd/yyyy"))

# Sort by 'Sort' ascending and 'Views (L90D)' descending
result = result.orderBy("Sort", desc("Views (L90D)"))

# Drop duplicates, keeping the most recent record for each dataset_id (based on Views (L90D))
window_spec = Window.partitionBy("dataset_id").orderBy(desc("Views (L90D)"))
result = (
    result.withColumn("row_num", row_number().over(window_spec))
    .filter(col("row_num") == 1)
    .drop("row_num")
)

# Define the output filename
ticket_number = "5121"
output_filename = f"DS{ticket_number}_{current_date.strftime('%m%d%Y')}_merged_v5.csv"

# Write the result to a CSV file
result.write.csv(output_filename, header=True)

# Show the result (optional)
result.show()

# Stop the Spark session
spark.stop()
