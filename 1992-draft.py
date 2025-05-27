import pandas as pd
from pathlib import Path

# File paths
input_csv = Path("players_1992.csv")  # Replace with your CSV file path

# Load the CSV file
try:
    players_df = pd.read_csv(input_csv)
except FileNotFoundError:
    print(f"File not found: {input_csv}")
    exit(1)

# Display the first few rows of the player stats
print("Available Players:")
print(players_df.head())

# Initialize teams
teams = {}
num_teams = int(input("Enter the number of teams: "))
for i in range(1, num_teams + 1):
    team_name = input(f"Enter the name of Team {i}: ")
    teams[team_name] = []

# Function to calculate standings
def calculate_standings(teams):
    standings = {}
    for team_name, players in teams.items():
        if players:
            team_df = pd.concat(players)
            # Sum up stats for each team (adjust Stat1, Stat2, etc., as needed)
            total_stats = team_df[["Stat1", "Stat2"]].sum().to_dict()
            standings[team_name] = total_stats
        else:
            standings[team_name] = {"Stat1": 0, "Stat2": 0}  # Default if no players picked

    # Calculate points based on rankings
    points = {team: 0 for team in teams.keys()}
    for stat in ["Stat1", "Stat2"]:
        sorted_teams = sorted(standings.items(), key=lambda x: x[1][stat], reverse=True)
        for rank, (team_name, _) in enumerate(sorted_teams, start=1):
            points[team_name] += len(teams) - rank + 1  # Assign points based on rank

    return points

# Draft players
print("\nStarting the draft...")
while not players_df.empty:
    for team_name in teams.keys():
        print(f"\nAvailable Players:")
        print(players_df[["Name", "Position", "Team", "Stat1", "Stat2"]])  # Adjust columns as needed
        player_name = input(f"{team_name}, pick a player by name (or type 'skip' to skip): ").strip()

        if player_name.lower() == "skip":
            continue

        # Check if the player exists
        if player_name in players_df["Name"].values:
            # Assign the player to the team
            player = players_df[players_df["Name"] == player_name]
            teams[team_name].append(player)
            # Remove the player from the available list
            players_df = players_df[players_df["Name"] != player_name]
        else:
            print(f"Player '{player_name}' not found. Please pick a valid player.")

        # Stop the draft if no players are left
        if players_df.empty:
            print("\nNo more players available. Draft is complete!")
            break

    # Calculate and display standings after each round
    current_standings = calculate_standings(teams)
    print("\nCurrent Standings (Points):")
    for team_name, points in current_standings.items():
        print(f"{team_name}: {points}")

# Final standings
print("\nFinal Standings:")
final_standings = calculate_standings(teams)
for team_name, points in final_standings.items():
    print(f"{team_name}: {points}")