from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
import os

# Initialize Spark session
spark = SparkSession.builder.appName("ProcessJSONFiles").getOrCreate()


def process_json_files(directory):
    # List all JSON files in the directory
    input_files = [f for f in os.listdir(directory) if f.endswith(".json")]

    for i, input_file in enumerate(input_files, start=1):
        file_path = os.path.join(directory, input_file)

        # Load JSON file as DataFrame
        df = spark.read.json(file_path, multiLine=True)

        # Add a column with the filename
        df = df.withColumn("source_file", lit(input_file))

        # Filter out undesired patterns
        df_filtered = df.filter(
            ~col("salesforce_response_metrics").isNotNull()
            & ~col("input_file").isNotNull()
        )

        # Flatten SalesforceResponse fields, if it exists
        if "SalesforceResponse" in df.columns:
            salesforce_cols = [
                col(f"SalesforceResponse.{key}").alias(f"SalesforceResponse_{key}")
                for key in df.select("SalesforceResponse.*").columns
            ]
            df_filtered = df_filtered.drop("SalesforceResponse").select(
                "*", *salesforce_cols
            )

        # Save the filtered data to a CSV file
        csv_file = os.path.join(directory, f"extracted_data_{i}.csv")
        if df_filtered.count() > 0:
            df_filtered.coalesce(1).write.csv(csv_file, header=True, mode="overwrite")
            print(
                f"Data from {input_file} has been processed and saved as CSV: {csv_file}"
            )
        else:
            print(f"No valid data to write to CSV for file {input_file}.")

        # Load the saved CSV into another DataFrame
        df_csv = spark.read.csv(csv_file, header=True, inferSchema=True)

        # Filter DataFrame for entries where SalesforceResponse_success is "false"
        if "SalesforceResponse_success" in df_csv.columns:
            results_df = df_csv.filter(col("SalesforceResponse_success") == "false")

            # Write the filtered error data to another CSV file
            error_csv_file = os.path.join(directory, f"finalerrorfile_{i}.csv")
            if results_df.count() > 0:
                results_df.coalesce(1).write.csv(
                    error_csv_file, header=True, mode="overwrite"
                )
                print(
                    f"Error-only CSV file created for {input_file} as {error_csv_file}"
                )


# Example usage
directory_path = "."  # Replace with the path to your JSON files directory
process_json_files(directory_path)

# Stop Spark session after processing
spark.stop()
