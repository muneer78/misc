import sqlparse
from pathlib import Path


def format_sql_file(input_file, output_file):
    input_path = Path(input_file)
    output_path = Path(output_file)

    with input_path.open("r", encoding="utf-8") as file:
        sql_content = file.read()

    formatted_sql = sqlparse.format(sql_content, reindent=True, keyword_case="upper")

    with output_path.open("w", encoding="utf-8") as file:
        file.write(formatted_sql)


# Example usage
input_file = "/Users/muneer78/Downloads/cadence-matillion-check.sql"
output_file = "/Users/muneer78/Downloads/cadence-matillion-check-updated.sql"
format_sql_file(input_file, output_file)
