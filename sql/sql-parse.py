import sqlfluff
from pathlib import Path


def format_sql_file(input_file, output_file):
    input_path = Path(input_file)
    output_path = Path(output_file)

    with input_path.open("r", encoding="utf-8") as file:
        sql_content = file.read()

    # Format the SQL content using sqlfluff
    formatted_sql = sqlfluff.fix(
        sql_content,
        rules=[
            "L002",
            "L003",
            "L004",
            "L010",
            "L015",
            "L016",
            "L019",
            "L030",
            "L034",
            "L036",
            "L041",
            "L065",
        ],
    )

    # Ensure that records in IN statements are not put on separate lines
    formatted_sql = formatted_sql.replace("IN (\n", "IN (").replace(",\n", ", ")

    # Remove whitespace in the IN clause
    formatted_sql = formatted_sql.replace(
        "',                                        '", "', '"
    )

    with output_path.open("w", encoding="utf-8") as file:
        file.write(formatted_sql)


# Example usage
input_file = r"C:\Users\mahmad\AppData\Roaming\DBeaverData\workspace6\General\Scripts\Script-1.sql"
output_file = r"C:\Users\mahmad\AppData\Roaming\DBeaverData\workspace6\General\Scripts\Script-updated.sql"
format_sql_file(input_file, output_file)

print("Formatted SQL file saved to:", output_file)
