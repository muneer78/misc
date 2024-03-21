def compare_strings(str1, str2):
    words1 = str1.split()
    words2 = str2.split()

    for i, (word1, word2) in enumerate(zip(words1, words2), start=1):
        if word1 != word2:
            print(f"Difference found at word {i}:")
            print(f"String 1: {word1}")
            print(f"String 2: {word2}\n")

    # Check if any additional words exist in str2
    if len(words2) > len(words1):
        for j in range(len(words1), len(words2)):
            print(f"Additional word in String 2 (word {j + 1}): {words2[j]}")

# Example usage
string1 = """{
    "Factorsoft_Client_Number__c": "138019REC",
    "Sub_Account__c": null,
    "First_Funding_Date__c": "2022-10-28",
    "Last_Funding_Date__c": "2023-10-23",
    "Balance__c": "0.0000",
    "Active__c": "false",
    "Fuel_Status_Group_Code__c": "IN COMPLIANCE",
    "Fuel_Card_Group_Code__c": "PILOT BUNDLE/SHAMROCK/IN NETWORK",
    "Pilot_Travel_Centers_LLC_Broker_Code__c": "true",
    "Account_Rep__c": "EXIT USER",
    "Cadence_Supervisor__c": "EXIT GROUP",
    "Cadence_Operations_Manager__c": null,
    "Exit_Code__c": "Buyout - Client Directed",
    "Exit_Date__c": "2023-12-28",
    "Exit_Notes__c": "12/28/23 - CARRIER STATED THEY ARE IN THE PROCESS OF CLOSING DOWN RV APPROVED $0 SLEF BUYOUT & FUNDS NEED TO BE HELD FOR PREFERENCE - TD    12/28/23 - NEED TO HOLD $4500 FOR PREFERENCE UNTIL 2/13/2024 - TD    12/28/23 - ISSUED GENERAL RL - TD",
    "Competitor_Moved_To__c": "SELF BUYOUT",
    "WO_Reason__c": null,
    "Write_Off__c": null,
    "Client_Credit_Rating__c": "E",
    "First_Fund_Exceptions__c": null,
    "UCC_Filing_Group_Code__c": null,
    "Last_Month_Volume__c": "0.00",
    "SalesforceResponse": {
        "created": false,
        "errors": [
            {
                "message": "We can't save this record because the \u201cSTC Cadence Details Create/Update\u201d process failed. Give your Salesforce admin these details. This error occurred when the flow tried to update records: FIELD_FILTER_VALIDATION_EXCEPTION: Contract must belong to the same account, must not be inactive, and must have a Bundle Starting Rate.. You can look up ExceptionCode values in the SOAP API Developer Guide. Error ID: 1064190376-681258 (954367962)ok up ExceptionCode values in the SOAP API Developer Guide. Error ID: 1064190376-681258 (954367962)",
                "errorCode": "CANNOT_EXECUTE_FLOW_TRIGGER",
                "fields": []
            }
        ],
        "id": null,
        "success": false
    }
}"""
string2 = """{
    "Factorsoft_Client_Number__c": "138019REC",
    "Sub_Account__c": null,
    "First_Funding_Date__c": "2022-10-28",
    "Last_Funding_Date__c": "2023-10-23",
    "Balance__c": "0.0000",
    "Active__c": "false",
    "Fuel_Status_Group_Code__c": "IN COMPLIANCE",
    "Fuel_Card_Group_Code__c": "PILOT BUNDLE/SHAMROCK/IN NETWORK",
    "Pilot_Travel_Centers_LLC_Broker_Code__c": "true",
    "Account_Rep__c": "EXIT USER",
    "Cadence_Supervisor__c": "EXIT GROUP",
    "Cadence_Operations_Manager__c": null,
    "Exit_Code__c": "Buyout - Client Directed",
    "Exit_Date__c": "2023-12-28",
    "Exit_Notes__c": "12/28/23 - CARRIER STATED THEY ARE IN THE PROCESS OF CLOSING DOWN RV APPROVED $0 SLEF BUYOUT & FUNDS NEED TO BE HELD FOR PREFERENCE - TD    12/28/23 - NEED TO HOLD $4500 FOR PREFERENCE UNTIL 2/13/2024 - TD    12/28/23 - ISSUED GENERAL RL - TD",
    "Competitor_Moved_To__c": "SELF BUYOUT",
    "WO_Reason__c": null,
    "Write_Off__c": null,
    "Client_Credit_Rating__c": "E",
    "First_Fund_Exceptions__c": null,
    "UCC_Filing_Group_Code__c": null,
    "Last_Month_Volume__c": "0.00",
    "SalesforceResponse": {
        "created": false,
        "errors": [
            {
                "message": "We can't save this record because the \u201cSTC Cadence Details Create/Update\u201d process failed. Give your Salesforce admin these details. This error occurred when the flow tried to update records: FIELD_FILTER_VALIDATION_EXCEPTION: Contract must belong to the same account, must not be inactive, and must have a Bundle Starting Rate.. You can look up ExceptionCode values in the SOAP API Developer Guide. Error ID: 1612275332-59492 (954367962)ook up ExceptionCode values in the SOAP API Developer Guide. Error ID: 1612275332-59492 (954367962)",
                "errorCode": "CANNOT_EXECUTE_FLOW_TRIGGER",
                "fields": []
            }
        ],
        "id": null,
        "success": false
    }
}"""

compare_strings(string1, string2)