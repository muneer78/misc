import pandas as pd
import random

# Load the CSV file containing the matchups and cutoff probabilities
key_value_pairs = pd.read_csv('seedrecords.csv', index_col=0)

def simulate_matchup(team1, team2, key_value_pairs):
    random_number = random.random()  # Generate a random number between 0 and 1
    # Retrieve the cutoff probability from key_value_pairs
    cutoff_prob = key_value_pairs.loc[f'{team1}-{team2}', 'Value']
    if random_number > cutoff_prob:
        return team1
    else:
        return team2

# Define the initial matchups for each region
east_matchups = ['1-16', '8-9', '5-12', '4-13', '6-11', '3-14', '7-10', '2-15']
west_matchups = ['1-16', '8-9', '5-12', '4-13', '6-11', '3-14', '7-10', '2-15']
south_matchups = ['1-16', '8-9', '5-12', '4-13', '6-11', '3-14', '7-10', '2-15']
midwest_matchups = ['1-16', '8-9', '5-12', '4-13', '6-11', '3-14', '7-10', '2-15']

# Determine the winner of the Midwest region (Region 1)
midwest_winner = None
if random.random() > 0.5:
    midwest_winner = simulate_matchup('1-16', '8-9', key_value_pairs)
    east_matchups.append(midwest_winner)
else:
    midwest_winner = simulate_matchup('1-16', '8-9', key_value_pairs)
    west_matchups.append(midwest_winner)

# Allow user input for which region will play against the Midwest
print("Which region will play against the Midwest? Enter 'E' for East, 'W' for West, or 'S' for South:")
user_input = input().upper()

# Validate user input
if user_input not in ['E', 'W', 'S']:
    print("Invalid input. Please enter 'E' for East, 'W' for West, or 'S' for South.")
    exit()

# Determine the remaining two regions
remaining_regions = ['East', 'West', 'South']
remaining_regions.remove({'E': 'East', 'W': 'West', 'S': 'South'}[user_input])

region_2 = remaining_regions.pop(random.randint(0, 1))
region_3 = remaining_regions[0]

# Simulate matchups for each region
east_winner = simulate_matchup(east_matchups[0], east_matchups[1], key_value_pairs)
west_winner = simulate_matchup(west_matchups[0], west_matchups[1], key_value_pairs)
south_winner = simulate_matchup(south_matchups[0], south_matchups[1], key_value_pairs)
midwest_winner = simulate_matchup(midwest_matchups[0], midwest_matchups[1], key_value_pairs)

# Determine the winner between the remaining two regions (Region 2 and Region 3)
region_2_winner = None
region_3_winner = None
if random.random() > 0.5:
    region_2_winner = midwest_winner
    region_3_winner = simulate_matchup(region_3, region_2, key_value_pairs)
else:
    region_2_winner = simulate_matchup(region_2, region_3, key_value_pairs)
    region_3_winner = midwest_winner

# Determine the winner between the winners of Region 2, Region 3, and Midwest (Region 1)
final_region_winner = simulate_matchup(region_2_winner, region_3_winner, key_value_pairs)

# Print the final matchups and winners for each region
print("Final matchups and winners for each region:")
print("Final 2 in the East is:", east_matchups[0], ". Winner:", east_winner)
print("Final 2 in the West is:", west_matchups[0], ". Winner:", west_winner)
print("Final 2 in the South is:", south_matchups[0], ". Winner:", south_winner)
print("Final 2 in the Midwest is:", midwest_matchups[0], ". Winner:", midwest_winner)

# Print the winner of the overall tournament
print("The winner of the NCAA March Madness tournament is:", final_region_winner, "from Region", {'E': 'East', 'W': 'West', 'S': 'South'}[user_input])
