import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport
from skimpy import skim
import glob

ticket = input("Enter Jira ticket number: ")


def find_file(pattern):
    files = glob.glob("*.xlsx")
    for f in files:
        if pattern in f:
            return f


# Construct the filenames
regional_filename = find_file("Regional")
lang_filename = find_file("Language")


def read_excel_sheet(filename, sheet_name):
    return pd.read_excel(filename, sheet_name=sheet_name)


df_regional = read_excel_sheet(regional_filename, "TEMPLATE")
df_lang = read_excel_sheet(lang_filename, "TEMPLATE")

skim(df_regional)
skim(df_lang)

profile_regional = ProfileReport(
    df_regional, title=f"SAL-{ticket} Regional Opps Profile Report"
)
profile_lang = ProfileReport(df_lang, title=f"SAL-{ticket} Lang Opps Profile Report")

profile_regional.to_file(f"SAL-{ticket} Regional.html")
profile_lang.to_file(f"SAL-{ticket} Lang.html")

print("All Done")
