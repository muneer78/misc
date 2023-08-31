import pandas as pd

df1 = pd.read_excel('users.xlsx', sheet_name = 'User_info')
df2 = pd.read_excel('users.xlsx', sheet_name = 'purchase')

def xlookup(lookup_value, lookup_array, return_array, if_not_found:str = ''):
    match_value = return_array.loc[lookup_array == lookup_value]
    if match_value.empty:
        return f'"{lookup_value}" not found!' if if_not_found == '' else if_not_found

    else:
        return match_value.tolist()[0]

  df1['purchase'] = df1['User Name'].apply(xlookup, args = (df2['Customer'], df2['purchase']))
