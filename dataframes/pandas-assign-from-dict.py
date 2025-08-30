import pandas as pd
import numpy as np

df = pd.read_excel('20230424 Day 91 Scrub Output.xlsx', sheet_name=['Create Lead', 'Create Opp', 'Reassign Opp'])
df_leads = df.get('Create Lead')
df_newopps = df.get('Create Opp')
df_existingopps = df.get('Reassign Opp')

df_reps = pd.read_csv('RepList.csv')
rep_names = df_reps["Name"]
rep_territory_dict = dict(zip(df_reps.Name, df_reps.Bucket))
rep_id_dict = dict(zip(df_reps.Name, df_reps.ID))
df_leads['rep'] = None

def setterritory(df_leads):
    if df_leads['fmcsa_trucks'] > 40: return "40+"
    elif df_leads['state'] == 'AZ' and df_leads['fmcsa_trucks'] <= 9: return "AZ 1-9"
    elif df_leads['state'] == 'AZ' and (df_leads['fmcsa_trucks'] > 9 and df_leads['fmcsa_trucks'] < 26): return "AZ 10-25"
    elif df_leads['state'] == 'AZ' and (df_leads['fmcsa_trucks'] > 25 and df_leads['fmcsa_trucks'] < 41): return "AZ 26-40"
    elif df_leads['state'] == 'IL' and df_leads['fmcsa_trucks'] <= 9: return "IL 1-9"
    elif df_leads['state'] == 'IL' and (df_leads['fmcsa_trucks'] > 9 and df_leads['fmcsa_trucks'] < 26): return "IL 10-25"
    elif df_leads['state'] == 'IL' and (df_leads['fmcsa_trucks'] > 25 and df_leads['fmcsa_trucks'] < 41): return "IL 26-40"
    elif df_leads['state'] == 'GA' and df_leads['fmcsa_trucks'] <= 9: return "GA 1-9"
    elif df_leads['state'] == 'GA' and (df_leads['fmcsa_trucks'] > 9 and df_leads['fmcsa_trucks'] < 26): return "GA 10-25"
    elif df_leads['state'] == 'GA' and (df_leads['fmcsa_trucks'] > 25 and df_leads['fmcsa_trucks'] < 41): return "GA 26-40"
    elif df_leads['state'] == 'TN' and df_leads['fmcsa_trucks'] <= 9: return "TN 1-9"
    elif df_leads['state'] == 'TN' and (df_leads['fmcsa_trucks'] > 9 and df_leads['fmcsa_trucks'] < 26): return "TN 10-25"
    elif df_leads['state'] == 'TN' and (df_leads['fmcsa_trucks'] > 25 and df_leads['fmcsa_trucks'] < 41): return "TN 26-40"
    elif df_leads['state'] == 'TX' and df_leads['fmcsa_trucks'] <= 9: return "TX 1-9"
    elif df_leads['state'] == 'TX' and (df_leads['fmcsa_trucks'] > 9 and df_leads['fmcsa_trucks'] < 26): return "TX 10-25"
    elif df_leads['state'] == 'TX' and (df_leads['fmcsa_trucks'] > 25 and df_leads['fmcsa_trucks'] < 41): return "TX 26-40"
    elif df_leads['state'] not in ('AZ', 'GA', 'IL', 'TN' 'TX') and df_leads['fmcsa_trucks'] <= 9: return "NR 1-9"
    elif df_leads['state'] not in ('AZ', 'GA', 'IL', 'TN' 'TX') and (df_leads['fmcsa_trucks'] > 9 and df_leads['fmcsa_trucks'] < 26): return "NR 10-25"
    elif df_leads['state'] not in ('AZ', 'GA', 'IL', 'TN' 'TX') and (df_leads['fmcsa_trucks'] > 25 and df_leads['fmcsa_trucks'] < 41): return "NR 26-40"
    else: return "not processed"
    
 df_leads['bucket'] = df_leads.apply(setterritory, axis=1)

repdict = {'AZ 1-9': ['Brandon Homan'], 
           'GA 1-9': ['Gustavo Marquez', 'Junior Robert', 'Rosana Aboytes'], 
           'IL 1-9': ['Joe Knudson', 'Justin Wold', 'Rosana Aboytes'],
           'NR 1-9': ['Adam Capps', 'Adris Veney', 'Amanda Breting', 'August Ripley', 'Austin Hicks', 'Dalton Graves', 'Ethan Warren', 'Jacob Peterson', 'Jed Kent', 'Jonathan Motyka', 'Justin Bilombele', 'Nagi Williams', 'Tony Lee', 'Wade Hyatt'],
           'TN 1-9': ['Ryan Wendt'],
           'TX 1-9': ['Maria Contin Garcia', 'TJ Thompson'],
           'AZ 10-25': ['Emily Kamm'],
           'GA 10-25': ['Holden Stallbaumer'],
           'IL 10-25': ['Connor Sacks', 'Richard Azunna-Iwuh'],
           'NR 10-25': ['Dylan Curry', 'Ethan Sageser', 'Nolan McCall', 'Robbie Genau', 'Tony Vitale'],
           'TN 10-25': ['Cole Theodoropoulos'],
           'TX 10-25': ['Landry Brewton'],
           'AZ 26-40': ['Emily Kamm'],
           'GA 26-40': ['Holden Stallbaumer'],
           'IL 26-40': ['Ashli Hill'],
           'NR 26-40': ['Jacob Douglas', 'Lucas Deegan', 'Seth Holman'],
           'TN 26-40': ['Jon Kiger'],
           'TX 26-40': ['Landry Brewton'],
           '40+': ['Matt Bernard']
          } 

# Iterate over the keys in the dictionary 
for bucket, values in repdict.items(): 
    # Get the row index where the key is present in the 'key' column 
    row_index = np.where(df_leads['bucket'] == bucket)
   
    value_num = 0
    for rowi in row_index[0]:
# Assign one of the values from the value list in the dictionary to the 'value' column at the row index 

        df_leads.iloc[rowi, 14] = values[value_num]
    
        if len(values) == value_num + 1:
            value_num = 0
        else:
            value_num +=1

df_leads['Contact Attempted'] = "No"
df_leads['Lead Status'] = "New"
df_leads['Campaign'] = "7013x000002LHUAAA4"
df_leads['Topic of Interest'] = "RTS Carrier Services"
df_leads['Lead Record Type'] = "0121H000001a2ShQAI"          
          
df_leads['repid'] = df_leads['rep'].map(rep_id_dict)

df_leads.to_csv('Day91Leads.csv',index=False)
