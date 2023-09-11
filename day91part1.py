import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

repdict = {'AZ 1-5': ['Kevin Kula'], 
           'GA 1-5': ['Rosana Aboytes', 'Gustavo Marquez'], 
           'IL 1-5': ['Ivan Beran', 'Joe Knudson'],
           'NR 1-9': ['Adan Baltazar', 'Amanda Breting', 'August Ripley', 'Derrick Cook', 'Dalton Graves', 'Dylan Curry', 'Ethan Warren', 'Gretchen Halldin', 'Harrison Porter', 'Jed Kent', 'Noah Durham', 'Rylan Chaney', 'Wade Hyatt'],
           'TN 1-5': ['Nick Price'],
           'TX 1-5': ['Lexi Kump', 'TJ Thompson'],
           'AZ 6-15': ['Emily Kamm'],
           'GA 6-15': ['Junior Robert'],
           'IL 6-15': ['James Sowa'],
           'NR 10-25': ['Alex Samuelson', 'Dylan Curry'],
           'TN 6-15': ['Michael Licciardi'],
           'TX 6-15': ['Landry Brewton'],
           'AZ 16-40': ['Emily Kamm'],
           'GA 16-40': ['Gustavo Marquez'],
           'IL 16-40': ['Ashli Hill'],
           'NR 26-40': ['Alex Samuelson', 'Jacob Douglas', 'Lucas Deegan', 'Brian Dolan'],
           'TN 16-40': ['Jon Kiger'],
           'TX 16-40': ['Landry Brewton'],
           '40+': ['Matt Bernard']
          }

state_to_code = {
    "ALABAMA": "AL",
    "ALASKA": "AK",
    "ARIZONA": "AZ",
    "ARKANSAS": "AR",
    "CALIFORNIA": "CA",
    "COLORADO": "CO",
    "CONNECTICUT": "CT",
    "DELAWARE": "DE",
    "DISTRICT OF COLUMBIA": "DC",
    "FLORIDA": "FL",
    "GEORGIA": "GA",
    "GUAM": "GU",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "ILLINOIS": "IL",
    "INDIANA": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KENTUCKY": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MICHIGAN": "MI",
    "MINNESOTA": "MN",
    "MISSISSIPPI": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "NEBRASKA": "NE",
    "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM",
    "NEW YORK": "NY",
    "NORTH CAROLINA": "NC",
    "NORTH DAKOTA": "ND",
    "NORTHERN MARIANA ISLANDS": "MP",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OREGON": "OR",
    "PENNSYLVANIA": "PA",
    "PUERTO RICO": "PR",
    "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD",
    "TENNESSEE": "TN",
    "TEXAS": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGIN ISLANDS": "VI",
    "VIRGINIA": "VA",
    "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV",
    "WISCONSIN": "WI",
    "WYOMING": "WY",
    "ALBERTA": "AB",
    "BRITISH COLUMBIA": "BC",
    "MANITOBA": "MB",
    "NEW BRUNSWICK": "NB",
    "NEWFOUNDLAND AND LABRADOR": "NL",
    "NORTHWEST TERRITORIES": "NT",
    "NOVA SCOTIA": "NS",
    "NUNAVUT": "NU",
    "ONTARIO": "ON",
    "PRINCE EDWARD ISLAND": "PE",
    "QUEBEC": "QC",
    "SASKATCHEWAN": "SK",
    "YUKON": "YT",
}

def read_excel_sheet(filename, sheet_name):
    return pd.read_excel(filename, sheet_name=sheet_name)

def setterritory(df):
    state = df['state']
    fmcsa_trucks = df['fmcsa_trucks']
    
    if fmcsa_trucks > 40:
        return "40+"
    elif state in ('AZ', 'IL', 'GA', 'TN', 'TX'):
        if fmcsa_trucks <= 5:
            return f"{state} 1-5"
        elif 6 <= fmcsa_trucks <= 15:
            return f"{state} 6-15"
        elif 16 <= fmcsa_trucks <= 40:
            return f"{state} 16-40"
    elif fmcsa_trucks <= 9:
        return "NR 1-9"
    elif 10 <= fmcsa_trucks <= 25:
        return "NR 10-25"
    elif 26 <= fmcsa_trucks <= 40:
        return "NR 26-40"
    else:
        return "not processed"

def assign_reps(row, repdict, rep_id_dict, assigned_reps):
    bucket = row['bucket']
    values = repdict.get(bucket, [])
    
    if values:
        assigned_index = assigned_reps.setdefault(bucket, 0)
        rep_index = assigned_index % len(values)
        
        row['rep'] = values[rep_index]
        row['repid'] = rep_id_dict.get(row['rep'], None)  # Add 'repid' column
        assigned_reps[bucket] += 1
        
    return row


def assign_and_filter_leads(df_leads, repdict, rep_id_dict):
    df_leads['rep'] = None
    df_leads['bucket'] = df_leads.apply(setterritory, axis=1)
    df_leads['repid'] = df_leads['rep'].map(rep_id_dict)

    # Define the list of Canadian provinces and territories
    canadian_provinces = (
    "AB",  # Alberta
    "BC",  # British Columbia
    "MB",  # Manitoba
    "NB",  # New Brunswick
    "NL",  # Newfoundland and Labrador
    "NS",  # Nova Scotia
    "NT",  # Northwest Territories
    "NU",  # Nunavut
    "ON",  # Ontario
    "PE",  # Prince Edward Island
    "QC",  # Quebec
    "SK",  # Saskatchewan
    "YT"   # Yukon
)

    # Had to remove Coahuila, Michoacan and Morelos from the list below because they have the same code as US states
    mexican_provinces = (
    "AG",  # Aguascalientes
    "BC",  # Baja California
    "BS",  # Baja California Sur
    "CM",  # Campeche
    "CS",  # Chiapas
    "CH",  # Chihuahua
    "CL",  # Colima
    "DG",  # Durango
    "GT",  # Guanajuato
    "GR",  # Guerrero
    "HG",  # Hidalgo
    "JC",  # Jalisco
    "MC",  # Mexico City (Ciudad de Mexico)
    "NT",  # Nayarit
    "NL",  # Nuevo León
    "OA",  # Oaxaca
    "PU",  # Puebla
    "QE",  # Querétaro
    "QR",  # Quintana Roo
    "SL",  # San Luis Potosí
    "SI",  # Sinaloa
    "SO",  # Sonora
    "TB",  # Tabasco
    "TM",  # Tamaulipas
    "TL",  # Tlaxcala
    "VE",  # Veracruz
    "YU",  # Yucatán
    "ZA"   # Zacatecas
    )

    # Create a dictionary to map states to country codes
    state_to_country_code = {
        'AZ': 'US',
        'IL': 'US',
        'GA': 'US',
        'TN': 'US',
        'TX': 'US'
    }

    # Function to get the country code based on the state
    def get_country_code(row):
        state = row['state']
        if state in canadian_provinces:
            return 'CA'
        elif state in mexican_provinces:
            return 'MX'
        elif state in state_to_country_code:
            return state_to_country_code[state]
        else:
            return 'US'

    # Apply the get_country_code function to create the "Country Code" column
    df_leads['Country Code'] = df_leads.apply(get_country_code, axis=1)

    # Now, update the 'rep' and 'repid' columns based on the 'bucket'
    df_leads = df_leads.apply(assign_reps, args=(repdict, rep_id_dict, assigned_reps), axis=1)
    df_leads_filtered = df_leads[df_leads['fmcsa_trucks'] < 250].copy()
    df_leads_filtered = df_leads_filtered.reset_index(drop=True)
    return df_leads_filtered

def update_state_names(df):
    df['state'] = df['state'].str.upper()  # Convert state names to uppercase
    df['state'] = df['state'].apply(lambda x: state_to_code.get(x, x))  # Map state names to state codes if available, else leave as-is
    return df

def update_lead_columns(df_leads, campaign_id):
    df_leads['Contact Attempted'] = "No"
    df_leads['Lead Status'] = "New"
    df_leads['Campaign'] = campaign_id
    df_leads['Topic of Interest'] = "RTS Carrier Services"
    df_leads['Lead Record Type'] = "0121H000001a2ShQAI"
    df_leads = df_leads[df_leads.fmcsa_trucks < 250]
    return df_leads

def create_and_export_csv(df, filename_prefix):
    date = dt.now().strftime("%Y-%m-%d")
    df.to_csv(f'{date}-{filename_prefix}.csv', index=False)

def process_opportunities(df_opps, campaign_id, opp_type, stage_name):
    df_opps['rep'] = None
    df_opps['bucket'] = df_opps.apply(setterritory, axis=1)
    df_opps = df_opps.apply(assign_reps, args=(repdict, rep_id_dict, assigned_reps), axis=1)
    future_date = (dt.now() + relativedelta(months=1)).strftime("%m/%d/%Y")
    df_opps['Close Date'] = future_date
    df_opps['Primary Source Campaign ID'] = campaign_id
    df_opps['Opportunity Type'] = "RTSCS"
    df_opps['RecordTypeId'] = "0123x000001dXL2AAM"
    df_opps['StageName'] = stage_name
    df_opps = df_opps[df_opps.fmcsa_trucks < 250]
    create_and_export_csv(df_opps, f'Day91{opp_type}')

def process_and_export_exceptions(df_opps_error):
    df_opps_error['rep'] = None
    df_opps_error['bucket'] = df_opps_error.apply(setterritory, axis=1)
    df_opps_error = df_opps_error.apply(assign_reps, args=(repdict, rep_id_dict, assigned_reps), axis=1)
    df_opps_error = df_opps_error[df_opps_error.fmcsa_trucks < 250]
    
    with pd.ExcelWriter(f'{date}-Day91Exceptions.xlsx') as writer:
        df_opps_error.to_excel(writer, sheet_name='Opportunities', index=False)

# Load data
filename = 'pfj_day_91_scrub_output_202309070928.xlsx'
sheet_names = ['Create Lead', 'Create Opp', 'Create Opp - Exception', 'Reassign Opp']
dfs = {sheet_name: read_excel_sheet(filename, sheet_name) for sheet_name in sheet_names}
df_leads = dfs['Create Lead']
df_newopps = dfs['Create Opp']
df_newoppserror = dfs['Create Opp - Exception']
df_existingopps = dfs['Reassign Opp']

# Update state names in dataframes
dfs['Create Lead'] = update_state_names(dfs['Create Lead'])
dfs['Create Opp'] = update_state_names(dfs['Create Opp'])
dfs['Create Opp - Exception'] = update_state_names(dfs['Create Opp - Exception'])
dfs['Reassign Opp'] = update_state_names(dfs['Reassign Opp'])

# Load rep_id_dict from CSV or define it here
df_reps = pd.read_csv('RepList.csv')
rep_id_dict = dict(zip(df_reps.Name, df_reps.ID))

# Initialize assigned_reps dictionary
assigned_reps = {}

# Get the current date
current_date = dt.now()

# Format the date as YYYYMMDD
date = current_date.strftime('%Y%m%d')

# Apply assign_reps function and filter leads
df_leads_filtered = assign_and_filter_leads(df_leads, repdict, rep_id_dict)

# Update lead columns
campaign_id = "7013x000002LHUAAA4"
df_leads_updated = update_lead_columns(df_leads_filtered, campaign_id)

# Export leads to CSV
create_and_export_csv(df_leads_updated, 'Day91Leads')

# Process new opportunities
process_opportunities(df_newopps, campaign_id, "NewOpps", "Open")

# Process existing opportunities
process_opportunities(df_existingopps, campaign_id, "ReassignOpps", "Open")

# Process new opportunities with errors and export exceptions
process_and_export_exceptions(df_newoppserror)