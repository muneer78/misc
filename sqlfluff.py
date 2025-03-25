import subprocess
from pathlib import Path

def format_sql_file(input_file, output_file):
    input_path = Path(input_file)
    output_path = Path(output_file)

    # Read the content of the input file
    with input_path.open('r', encoding='utf-8') as file:
        sql_content = file.read()

    # Write the content to a temporary file
    temp_input_path = input_path.with_suffix('.tmp.sql')
    with temp_input_path.open('w', encoding='utf-8') as file:
        file.write(sql_content)

    # Format the SQL using sqlfluff
    subprocess.run(['sqlfluff', 'fix', str(temp_input_path), '--dialect', 'ansi', '--output', str(output_path)])

    # Remove the temporary file
    temp_input_path.unlink()

# Example usage
input_file = '/Users/muneer78/Downloads/cadence-matillion-check.sql'
output_file = '/Users/muneer78/Downloads/cadence-matillion-check-updated-2.sql'
format_sql_file(input_file, output_file)