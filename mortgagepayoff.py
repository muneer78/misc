import polars as pl
import numpy as np
import numpy_financial as npf
from datetime import date, timedelta
from plotnine import ggplot, aes, geom_bar, theme_minimal, labs, theme, element_text
import pandas as pd

# Initialize an empty DataFrame to store results
storage_df = pl.DataFrame()

# Loop through 1000 simulations
for x in range(1000):
    interest = 0.04125
    years = 1
    payments_year = 12
    mortgage = 35763.56
    start_date = date(2023, 4, 1)
    end_date = start_date + timedelta(days=years * 365)

    initial_pmt = 965.99
    initial_ipmt = -1 * npf.ipmt(interest / payments_year, 1, years * payments_year, mortgage)
    initial_ppmt = -1 * npf.ppmt(interest / payments_year, 1, years * payments_year, mortgage)

    # Create date range as an expression
    rng_expr = pl.date_range(start=start_date, end=end_date, interval='1mo')

    # Create date range as a list of Python datetime objects
    rng_py = pl.date_range(start=start_date, end=end_date, interval='1mo').collect().to_list()

    # Create DataFrame with initial values
    df = pl.DataFrame({
        'Payment Date': rng_py,
        'Org Total Payment': pl.Series([initial_pmt] * len(rng_py)),
        'Total Payment': pl.Series([initial_pmt] * len(rng_py)),
        'Interest': pl.Series([initial_ipmt] * len(rng_py)),
        'Principal': pl.Series([initial_ppmt] * len(rng_py)),
        'Additional Payment': pl.Series([0] * len(rng_py)),
        'Org Ending Balance': pl.Series([mortgage - initial_ppmt] * len(rng_py)),
        'Ending Balance': pl.Series([mortgage - initial_ppmt] * len(rng_py))
    })

    additional_pmt = np.random.randint(0, 3500, size=len(df))

    # Update DataFrame with additional payments
    df = df.with_columns([
        (pl.col('Total Payment') + additional_pmt).alias('Total Payment'),
        (pl.col('Org Ending Balance') - additional_pmt).alias('Ending Balance'),
        pl.Series('Additional Payment', additional_pmt)
    ])

    # Initialize rows list with the first row as a dictionary
    rows = [df.row(0, named=True)]

    # Update remaining rows
    for period in range(1, len(df)):
        previous_row = rows[-1]
        previous_org_ending_balance = previous_row['Org Ending Balance']
        previous_ending_balance = previous_row['Ending Balance']

        period_interest = previous_org_ending_balance * interest / payments_year
        period_principal = initial_pmt - period_interest
        additional_pmt = np.random.randint(1000, 3500) + 400
        org_ending_balance = previous_org_ending_balance - period_principal
        ending_balance = previous_ending_balance - period_principal - additional_pmt

        row = {
            'Payment Date': df['Payment Date'][period],
            'Org Total Payment': initial_pmt,
            'Total Payment': initial_pmt + additional_pmt,
            'Interest': period_interest,
            'Principal': period_principal,
            'Additional Payment': additional_pmt,
            'Org Ending Balance': org_ending_balance,
            'Ending Balance': ending_balance
        }
        rows.append(row)

    # Convert rows to DataFrame
    df = pl.DataFrame(rows)
    df = df.filter(pl.col('Ending Balance') >= 15000)
    last_row = df.tail(1)
    storage_df = storage_df.vstack(last_row)

finaldf = storage_df.select(['Payment Date', 'Ending Balance'])
finaldf.write_csv('allruns.csv')

df = pl.read_csv('allruns.csv')

df2 = df['Payment Date'].value_counts().sort('Payment Date')
df2.write_csv('payofftotals.csv')

# Plot using plotnine
plot = (
    ggplot(df2, aes(x='Payment Date', y='count')) +
    geom_bar(stat='identity') +
    theme_minimal() +
    theme(axis_text_x=element_text(rotation=90, hjust=1)) +
    labs(title='Payoff Totals by Payment Date', x='Payment Date', y='Count')
)

# Save the plot as a PDF
plot.save('PayoffGraph.pdf')