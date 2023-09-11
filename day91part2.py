import pandas as pd
from datetime import datetime as dt

def load_csv_file(file_name):
    return pd.read_csv(file_name)

def merge_and_cleanup_data(df_successleads, df_leads):
    merged_df = pd.merge(df_successleads, df_leads, left_on='PFJ_SF_NAME', right_on='pfj_sf_name')
    merged_df.drop('pfj_sf_name', axis=1, inplace=True)
    return merged_df

def export_data_to_excel(df_leads, df_newopps, df_existingopps, date):
    excel_file_name = f'{date}-Day91Load.xlsx'
    with pd.ExcelWriter(excel_file_name) as writer:
        df_leads.to_excel(writer, sheet_name='Leads', index=False)
        df_newopps.to_excel(writer, sheet_name='New Opportunities', index=False)
        df_existingopps.to_excel(writer, sheet_name='Reassigned Opportunities', index=False)

def main():
    date = dt.today().strftime('%Y-%m-%d')
    
    leads_file = f'{date}-Day91Leads.csv'
    newopps_file = f'{date}-Day91NewOpps.csv'
    existingopps_file = f'{date}-Day91ReassignOpps.csv'
    
    df_successleads = load_csv_file('success.csv')
    df_leads = load_csv_file(leads_file)
    df_newopps = load_csv_file(newopps_file)
    df_existingopps = load_csv_file(existingopps_file)
    
    merged_df = merge_and_cleanup_data(df_successleads, df_leads)
    
    export_data_to_excel(merged_df, df_newopps, df_existingopps, date)

if __name__ == "__main__":
    main()