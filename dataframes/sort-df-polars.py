import polars as pl
import os
from datetime import datetime as dt

# Get the current date
current_date = dt.now().strftime(
    "%Y%m%d"
)  # Format the date to avoid invalid characters

# Your file path
file = r"/Users/muneer78/Downloads/2026_Tourney_teams_only_actual.csv"

filename = os.path.splitext(os.path.basename(file))[0]

dforig = pl.read_csv(file)

# df_sorted = dforig.sort(['sf_object', 'int_field'], descending=[False, True])
df_sorted = dforig.sort(["summary_RankDE", "summary_RankOE"], descending=False)

ticket_number = "2307"
output_filename = f"{current_date}_output.csv"

df_sorted.write_csv(output_filename)

print("Done")
