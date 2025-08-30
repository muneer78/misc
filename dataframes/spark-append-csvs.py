from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a Spark session
spark = SparkSession.builder.appName("Append CSV Files").getOrCreate()

# List of CSV files to be appended
csv_files = ["finalerrorfile_1.csv", "finalerrorfile_2.csv", "finalerrorfile_3.csv"]


# Function to convert all columns to strings
def convert_to_strings(df):
    for col_name in df.columns:
        df = df.withColumn(col_name, col(col_name).cast("string"))
    return df


# Read all CSV files and convert all values to strings
df_list = [spark.read.csv(file, header=True, inferSchema=True) for file in csv_files]
df_list = [convert_to_strings(df) for df in df_list]

# Concatenate all DataFrames
appended_df = df_list[0]
for df in df_list[1:]:
    appended_df = appended_df.union(df)

# Save the concatenated DataFrame to a new CSV file
appended_df.write.csv("allerrors.csv", header=True, mode="overwrite")

print(
    "CSV files have been successfully appended and converted to strings using PySpark!"
)
