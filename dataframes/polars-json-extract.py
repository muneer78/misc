import json
import polars as pl

# Path to your JSON file
file_path = "cadence_clientkey_20240628172110562003.json"

# Initialize a list to collect the extracted data
extracted_data_list = []

# Read the JSON file line by line
with open(file_path, "r") as f:
    for line in f:
        # Load each line as a JSON object
        try:
            data = json.loads(line)
            # Extract the specific key-value pair
            extracted_data = {
                "Factorsoft_Client_Key__c": data.get("Factorsoft_Client_Key__c")
            }
            extracted_data_list.append(extracted_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

# Create a Polars DataFrame from the extracted data
df = pl.DataFrame(extracted_data_list)
sorted_df = df.sort("Factorsoft_Client_Key__c", descending=[False])
df.write_csv("factorsoftclientnos.csv")
print("Done")
