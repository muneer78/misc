import pandas as pd
import numpy as np
import numpy_financial as npf
from datetime import date, datetime
from numpy import random
import matplotlib.pyplot as plt

storage_df = pd.DataFrame()

for x in range(1000):
        interest = 0.04125
        years = 1
        payments_year = 12
        mortgage = 26239.82
        start_date=(date(2023, 5, 1))

        #initial_pmt = -1 * npf.pmt(interest / 12, years * payments_year, mortgage)
        initial_pmt = 965.99
        initial_ipmt = -1 * npf.ipmt(interest / payments_year, 1, years * payments_year, mortgage)
        initial_ppmt = -1 * npf.ppmt(interest / payments_year, 1, years * payments_year, mortgage)
        #print('Initial Payment: {:,.2f}'.format(initial_pmt))
        #print('Initial Interest: {:,.2f}'.format(initial_ipmt))
        #print('Initial Principal Payment: {:,.2f}'.format(initial_ppmt))


        # Create date range in pandas dataframe
        rng = pd.date_range(start_date, periods=years * payments_year, freq='MS')

        # label the date column
        rng.name="Payment Date"


        # create dataframe
        df=pd.DataFrame(
            index = rng,
            columns = ['Org Total Payment',
                      'Total Payment',
                      'Interest',
                      'Principal',
                      'Additional Payment',
                      'Org Ending Balance',
                      'Ending Balance'], dtype='float')
        # set index as payment period
        df.reset_index(inplace=True)
        df.index += 1
        df.index.name="Period"
        df['Payment Date'] = df['Payment Date'].dt.strftime('%m-%Y')

        # Create values for the first period
        period = 1
        additional_pmt = np.random.randint(0, 3500, size=len(df))

        # for each element in the row set the value
        initial_row_dict = {
            'Org Total Payment':initial_pmt,
            'Total Payment': initial_pmt + (additional_pmt),
            'Interest': initial_ipmt,
            'Principal':initial_ppmt,
            'Additional Payment': additional_pmt,
            'Org Ending Balance': mortgage - initial_ppmt,
            'Ending Balance': mortgage - initial_ppmt - (additional_pmt)
        }

        # set values
        columns = list(initial_row_dict.keys())
        period_values = list(initial_row_dict.values())
        df.at[period, columns]= period_values

        # add additional rows
        for period in range(2, len(df) + 1):
            #get prior period values
            previous_total_payment = df.loc[period - 1, 'Total Payment']
            previous_principal = df.loc[period - 1, 'Principal']
            previous_org_ending_balance = df.loc[period - 1, 'Org Ending Balance']
            previous_ending_balance = df.loc[period - 1, 'Ending Balance']
            #get end balance
            period_interest = previous_org_ending_balance * interest / payments_year
            period_principal = initial_pmt - period_interest
            additional_pmt = np.random.randint(1000, 3500) + 400
            org_ending_balance = previous_org_ending_balance - period_principal
            ending_balance = previous_ending_balance - period_principal - additional_pmt

            row_dict = {'Org Total Payment':initial_pmt,
                        'Total Payment': initial_pmt + (additional_pmt),
                        'Interest': period_interest,
                        'Principal': period_principal,
                        'Additional Payment': additional_pmt,
                        'Org Ending Balance': org_ending_balance,
                        'Ending Balance': ending_balance}
            columns = list(row_dict.keys())
            period_values = list(row_dict.values())
            df.at[period, columns]= period_values
            df_mask=df['Ending Balance']>=15000
            filtered_df = df[df_mask].round(2)
            last_row = filtered_df.tail(1)
        storage_df = storage_df.append(last_row, ignore_index=True)

finaldf= storage_df[["Payment Date", 'Ending Balance']]
finaldf.to_csv('allruns.csv')

df = pd.read_csv('allruns.csv')

df2 = []
df2 = df['Payment Date'].value_counts()

df = df.assign(PayoffAmount=df['Ending Balance'].astype(str).str[:2])
# df = df.assign(PayoffAmount=df['Ending Balance'].str[:2])
# df['PayoffAmount'] = df['Ending Balance'].astype(str).str[:2].astype(int)
df3 = df.groupby('PayoffAmount').count()
# Select the columns that you want to drop
columns_to_drop = ['Payment Date', 'Ending Balance']

# Drop the selected columns
df3 = df3.drop(columns_to_drop, axis=1)
df3.rename(columns={'Unnamed: 0': 'Count'})
print(df3)

list_of_dfs = [df2, df3]
with open('payoffanalytics.csv','w+', nrows=None) as f:
    for df in list_of_dfs:
        df.to_csv(f, index=True)
        f.write("\n")

plt.figure()
plt.xticks(rotation=180)
df2.plot.bar(x='Payment Date',y='val')
plt.tight_layout()
#plt.show()
plt.savefig('PayoffGraph.pdf')