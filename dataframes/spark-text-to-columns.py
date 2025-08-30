from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col
from datetime import datetime as dt

# Initialize Spark session
spark = SparkSession.builder.appName("Split and Expand Columns").getOrCreate()

# Get the current date
current_date = dt.now().strftime("%Y-%m-%d_%H-%M-%S")

# Sample data
data = [("John, Doe, 30",), ("Jane, Smith, 25",), ("Alice, Johnson, 40",)]
df = spark.createDataFrame(data, ["text_column"])

# Split the 'text_column' into multiple columns
split_df = df.withColumn("split_column", split(col("text_column"), ", "))

# Expand the 'split_column' into separate columns
expanded_df = (
    split_df.withColumn("col_1", col("split_column").getItem(0))
    .withColumn("col_2", col("split_column").getItem(1))
    .withColumn("col_3", col("split_column").getItem(2))
    .drop("split_column")
)

# Define the output filename
ticket_number = "insert Jira number here"
output_filename = f"DS{ticket_number}_{current_date}_output.csv"

# Save the resulting DataFrame to a CSV file
expanded_df.write.csv(output_filename, header=True)
