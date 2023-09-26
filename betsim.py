import pandas as pd
import numpy as np
import random

# Generate random odds between -295 and -110, or between +100 and +200
data = [random.randrange(-295, -110, 5) if random.random() < 0.5 else random.randrange(100, 201, 5) for i in range(100)]
df = pd.DataFrame(data, columns=['Odds'])

def format_currency(x):
    return "${:,.2f}".format(x)

np.random.seed(365)

# Generate random amounts between 0.10 and 5.00 in 0.05 increments
amounts = [round(random.randrange(2, 101) * 0.05, 2) for _ in range(100)]
df['Amount'] = amounts

# Generate random results ("W" for win or "L" for loss)
results = [random.choice(['W', 'L']) for _ in range(100)]
df['Result'] = results

odds = df["Odds"]
cleaned_odds = abs(df["Odds"])

# Calculate Profit based on Result
df["Profit"] = np.where(df['Result'] == 'L', df["Amount"] * -1, ((100 / cleaned_odds) * df["Amount"])).round(2)

df["Implied Probability"] = (cleaned_odds / (100 + cleaned_odds)).round(2)

df["EV"] = (df["Implied Probability"] * (df["Profit"])) - ((1-df["Implied Probability"])*((df["Amount"]*(-1))))
df["EV"] = df["EV"].round(2)
df["Long Term Profit"] = df["EV"] - df["Amount"]
df['Implied Probability'] = df['Implied Probability'].map(lambda n: '{:,.2%}'.format(n))

# Round all number columns to 2 decimal places
number_columns = ["Profit", "Amount", "EV", "Long Term Profit"]
df[number_columns] = df[number_columns].round(2)

# Calculate and add the Grand Total row
grand_total = df[["Profit", "Amount", "EV", "Long Term Profit"]].sum().to_frame().T
grand_total["Result"] = "Grand Total"
grand_total = grand_total[["Result", "Profit", "Amount", "EV", "Long Term Profit"]]

# Round all values in the Grand Total row to 2 decimal places
grand_total = grand_total.round(2)

df = pd.concat([df, grand_total], ignore_index=True)

# Format Amount, Profit, EV, and Long Term Profit columns as currency
currency_columns = ["Amount", "Profit", "EV", "Long Term Profit"]
df[currency_columns] = df[currency_columns].applymap(format_currency)

df.to_csv('betsim.csv')