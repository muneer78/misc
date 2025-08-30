import difflib
from pathlib import Path
from datetime import datetime as dt

# Get the current date and format it as 'yyyy-mm-dd'
current_date = dt.now().strftime("%Y-%m-%d")

first_file_lines = Path("DS4709old.txt").read_text().splitlines()
second_file_lines = Path("DS4709new.txt").read_text().splitlines()

# ticket_number = 'insert Jira number here'
ticket_number = "4709"
output_filename = f"DS{ticket_number}_{current_date}_chart.html"

html_diff = difflib.HtmlDiff().make_file(first_file_lines, second_file_lines)
Path(output_filename).write_text(html_diff)
