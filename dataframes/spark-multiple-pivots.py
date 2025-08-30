from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, count
from datetime import datetime as dt

# Initialize Spark session
spark = SparkSession.builder.appName("CSV Processing").getOrCreate()

# Get the current date
current_date = dt.now()

# Read the CSV file into a Spark DataFrame
df = spark.read.csv("DS4013-20240605.csv", header=True, inferSchema=True)

# Create 'cleanedclientno' column by removing non-numeric characters from 'clientno'
df = df.withColumn("cleanedclientno", regexp_replace("clientno", r"\D", ""))


# Function to create a grouped DataFrame
def create_grouped_df(df, column_name):
    return (
        df.groupBy(column_name)
        .agg(count(column_name).alias("count"))
        .orderBy("count", ascending=False)
    )


# Columns to analyze
columns = ["cleanedclientno", "acctexec", "masterclientkey"]

ticket_number = "insert Jira number here"
output_filename = f"DS{ticket_number}_{current_date.strftime('%Y%m%d')}_output"

# Save results to Excel files using Pandas (as Spark does not directly support Excel)
import pandas as pd

with pd.ExcelWriter(f"{output_filename}.xlsx", engine="openpyxl") as writer:
    for column in columns:
        # Create grouped DataFrame
        grouped_df = create_grouped_df(df, column)

        # Convert grouped DataFrame to Pandas DataFrame for Excel writing
        pandas_df = grouped_df.toPandas()

        # Write the DataFrame to a new sheet
        pandas_df.to_excel(writer, sheet_name=f"{column}_counts", index=False)

print("Dataframes have been created and saved to output.xlsx")

# Stop the Spark session
spark.stop()
