from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, count

# Initialize Spark session
spark = SparkSession.builder.appName("CSV Processing").getOrCreate()

# Load the CSV file
input_path = "path/to/your/input.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Rename columns (e.g., renaming "oldName1" to "newName1", "oldName2" to "newName2")
renamed_df = df.withColumnRenamed("oldName1", "newName1").withColumnRenamed(
    "oldName2", "newName2"
)

# Replace whitespace in column 'A' with dashes
cleaned_df = renamed_df.withColumn("A", regexp_replace(col("A"), r"\s+", "-"))

# Filter rows (e.g., filter where column "age" is greater than 30)
filtered_df = cleaned_df.filter(col("age") > 30)

# Select specific columns to include in the output
selected_df = filtered_df.select(
    "A", "B", "C", "E", "F", "newName1", "newName2", "otherColumn"
)

# Drop duplicate rows based on selected columns
unique_df = selected_df.dropDuplicates()

# Group by column 'B' and aggregate (e.g., count the number of occurrences in each group)
grouped_df = unique_df.groupBy("B").agg(count("*").alias("count"))

# Sort by column 'C' in ascending order
sorted_df = grouped_df.orderBy("C", ascending=True)

# Add a new column 'D' with a calculation or constant value
final_df = sorted_df.withColumn("D", col("count") * 2)

# Count records in column 'E' (non-null values) and print to console
record_count_E = selected_df.filter(col("E").isNotNull()).count()
print(f"Number of records in column 'E': {record_count_E}")

# Conditional count for column 'F'
criteria = "desired_value"  # Replace with your actual criteria
conditional_count_F = selected_df.filter(col("F") == criteria).count()
print(
    f"Number of records in column 'F' with criteria '{criteria}': {conditional_count_F}"
)

# Write the transformed DataFrame to a new CSV file
output_path = "path/to/your/output.csv"
final_df.write.csv(output_path, header=True, mode="overwrite")

# Stop the Spark session
spark.stop()
