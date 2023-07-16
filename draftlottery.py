"""
Using random to generate order

Using csv to create csv file
    """

import random
import csv

# Define the teams and their corresponding odds
teams = {
    "Himes": 20,
    "Muneer": 15,
    "Brian": 10,
    "Lopez": 8,
    "Britt": 6,
    "Jack": 5,
    "Nick": 4,
    "Scott": 3,
    "Tony": 2,
    "Carl": 1,
}

# Calculate the total number of chances for all teams
total_chances = sum(teams.values())

# Pick a random number between 1 and the total number of chances
RANDOM_NUM = random.randint(1, total_chances)

# Determine which team is assigned the random number
COUNT_CHANCES = 0
WINNING_TEAM = None
for team, chances in teams.items():
    COUNT_CHANCES += chances
    if COUNT_CHANCES >= RANDOM_NUM:
        WINNING_TEAM = team
        print(f"The {WINNING_TEAM} has won the draft lottery!")
        break

# Remove the winning team from the list of teams and their chances
del teams[WINNING_TEAM]

# Re-calculate the total number of chances for the remaining teams
total_chances = sum(teams.values())

# Create a list of the remaining teams and their chances
# remaining_teams = [(team, chances) for team, chances in teams.items()]
remaining_teams = list(teams.items())

# Sort the remaining teams by their chances in descending order
remaining_teams.sort(key=lambda x: x[1], reverse=True)

# Determine the draft order for the remaining teams
draft_order = [] + [team[0] for team in remaining_teams]

# Print the final draft order
print("Final draft order:")
for i, team in enumerate(draft_order):
    print(f"{i+1}. {team}")

with open("draft_lottery_results.csv", mode="w", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Team", "Draft Order"])

    # Write the draft order to the CSV file
    writer.writerows([[team, i + 1] for i, team in enumerate(draft_order)])
