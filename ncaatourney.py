'''
Got code from https://www.linkedin.com/pulse/projecting-bracket-python-2023-drew-zeimetz/
'''


import pandas as pd
import statsmodels.api as sm

# Read in the data from a CSV file
data = pd.read_csv("Tournament Team Data.csv")
data2 = pd.read_csv('Tournament_Teams_2023_MM.csv')

# Get the unique values in the "ROUND" column
rounds = data["ROUND"].unique()

# Display the unique values
print(rounds)

# Display the expected value of wins by 'SEED'
expected_wins = data.groupby('SEED')['WINS'].mean()
print(expected_wins)

# Define a function to convert round numbers to wins
def round_to_wins(round_num):
    if round_num == 68 or round_num == 64:
        return 0
    elif round_num == 32:
        return 1
    elif round_num == 16:
        return 2
    elif round_num == 8:
        return 3
    elif round_num == 4:
        return 4
    elif round_num == 2:
        return 5
    elif round_num == 1:
        return 6
    else:
        return None


# Apply the function to create a new "WINS" column
data["WINS"] = data["ROUND"].apply(round_to_wins)

# Convert SEED to categorical variable
data['SEED'] = pd.Categorical(data['SEED'])


# Define the predictor variables
predictors = ['SEED', 'KENPOM ADJUSTED OFFENSE', 'KENPOM ADJUSTED DEFENSE']


# Define the response variable
response = 'WINS'


# Create the design matrix by adding a constant and selecting the predictor variables
X = sm.add_constant(pd.get_dummies(data[predictors]))


# Define the response variable
y = data[response]


# Fit the linear regression model
model = sm.OLS(y, X).fit()

# Use the model to predict the number of wins for each team
data2['PREDICTED WINS'] = model.predict(X)


# Save the results to a new file
data2.to_csv('Tournament_Teams_2023_MM_predicted.csv', index=False)