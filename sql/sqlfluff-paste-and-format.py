import sqlfluff
import subprocess


def copy2clip(txt):
    cmd = f"echo {txt.strip()} | clip"
    return subprocess.run(cmd, shell=True, check=True, text=True)


def format_sql_query(sql_query):
    # Format the SQL content using sqlfluff
    # formatted_sql = sqlfluff.fix(
    #     sql_query, rules=["L002", "L003", "L004", "L010", "L015", "L016", "L019", "L030", "L034", "L036", "L041", "L065"]
    # )

    formatted_sql = sqlfluff.fix(
        sql_query,
        rules=[
            "L001",
            "L002",
            "L003",
            "L004",
            "L005",
            "L006",
            "L008",
            "L010",
            "L012",
            "L015",
            "L016",
            "L019",
            "L023",
            "L024",
            "L027",
            "L030",
            "L034",
            "L036",
            "L039",
            "L041",
            "L047",
            "L048",
            "L049",
            "L063",
            "L065",
            "L067",
            "L071",
        ],
    )
    return formatted_sql


# Example usage
sql_query = """SELECT name, id, dot_number__c
FROM crm.rpl_lead rl 
WHERE name ilike 'stevephine%'

SELECT name, id, partner_entity_id__c, stc_transaction_id__c, dot_number__c, isconverted, isdeleted, company, lastmodifiedbyid 
FROM crm.rpl_lead rl 
WHERE dot_number__c = 3157841
"""

formatted_sql = format_sql_query(sql_query)
formatted_sql_str = str(formatted_sql)
print("Formatted SQL query:")
print(formatted_sql_str)

copy2clip(formatted_sql_str)
print("Formatted SQL query copied to clipboard.")
