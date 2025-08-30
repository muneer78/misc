text_with_line_breaks = """OR(
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "EFS"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
),
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "Fleet One"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6,7}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
),
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "RTS Fleet One"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
),
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "Titan - Bronze"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
),
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "Titan - Silver"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
),
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "Titan - Gold"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
),
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "Titan - Diamond"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
),
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "Titan - Emerald"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
),
AND(
$Profile.Name != "Shamrock-SA",
ISPICKVAL(Fuel_Card_Type__c, "Titan - Shamrock"),
NOT REGEX(Fuel_Account_Number__c,"[0-9]{6}$"),
NOT(ISBLANK( Fuel_Account_Number__c ))
)
)"""

# Remove spaces, line breaks, and carriage returns
text_without_line_breaks = (
    text_with_line_breaks.replace(" ", "").replace("\n", "").replace("\r", "")
)

print(text_without_line_breaks)
