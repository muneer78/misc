from pyspark.sql import SparkSession
import os


def search_in_files(search_string, directory):
    spark = SparkSession.builder.appName("File Search").getOrCreate()
    found_files = []
    files_searched = 0

    # List all files in the directory
    for file_name in os.listdir(directory):
        if "cadence" in file_name:
            files_searched += 1
            file_path = os.path.join(directory, file_name)

            # Read the file into a DataFrame
            df = spark.read.text(file_path)

            # Check if the search string exists in any line
            if df.filter(df.value.contains(search_string)).count() > 0:
                found_files.append(file_path)

    spark.stop()
    return found_files, files_searched


# Example usage:
search_string = input("Enter the string to search for: ")
directory = input("Enter the directory to search in: ")

found_files, files_searched = search_in_files(search_string, directory)
if found_files:
    print("Found in these files:")
    for file_path in found_files:
        print(file_path)
else:
    print("String not found in any files.")
print("Total files searched:", files_searched)
