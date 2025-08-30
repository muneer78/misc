import json

# JSON data
json_data = """[{"column": "pfj_ascend_number__c", "new_data_type": "IntegerType()", "old_data_type": "StringType()"}, {"column": "firstemaildatetime", "new_data_type": "StringType()", "old_data_type": "DateType()"}, {"column": "scheduledresumedatetime", "new_data_type": "StringType()", "old_data_type": "DateType()"}, {"column": "pfj_min_gallon_percentage__c", "new_data_type": "StringType()", "old_data_type": "DoubleType()"}, {"column": "lastvieweddate", "new_data_type": "StringType()", "old_data_type": "DateType()"}, {"column": "facebook_lead_id__c", "new_data_type": "LongType()", "old_data_type": "StringType()"}, {"column": "firstcalldatetime", "new_data_type": "StringType()", "old_data_type": "DateType()"}, {"column": "lastreferenceddate", "new_data_type": "StringType()", "old_data_type": "DateType()"}, {"column": "last_reassignment__c", "new_data_type": "StringType()", "old_data_type": "DateType()"}, {"column": "pfj_min_gallon_amount__c", "new_data_type": "StringType()", "old_data_type": "DoubleType()"}]
"""

# Parse the JSON data
data = json.loads(json_data)

# Remove "Type()" from all strings in the 'new_data_type' and 'old_data_type' fields
for item in data:
    item["new_data_type"] = item["new_data_type"].replace("Type()", "")
    item["old_data_type"] = item["old_data_type"].replace("Type()", "")

# Print the output in the specified format
for item in data:
    print(f"{item['column']}")
    print(f"DBX: {item['new_data_type']}")
    print(f"Redshift: {item['old_data_type']}")
