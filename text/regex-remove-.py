import re

string = """
SELECT "docketnbr" AS "mc_number__c", "dotnbr" AS "dot_number__c", "legalnm" AS "company_legal_name__c", "dbanm" AS "name", "physaddr" AS "physaddr", "physcity" AS "physcity", "physstate" AS "physstate", "physzip" AS "physzip", "physcountry" AS "physcountry", "physphonenbr" AS "physphonenbr", "description" AS "description", "email" AS "email", "topicofinterest" AS "topic_of_interest__c", "campaignid" AS "campaignid", "leadsource" AS "leadsource", "recordtypeid" AS "recordtypeid", "contact1firstnm" AS "contact1firstnm", "contact1lastnm" AS "contact1lastnm", "contact2firstnm" AS "contact2firstnm", "contact2lastnm" AS "contact2lastnm", "trucknbr" AS "trucknbr" FROM "$T{Calculator 3}"
"""

pattern = r"\(\$T\{([^}]*)\}\)"

result = re.sub(pattern, r"{\1}", string)

print(result)
