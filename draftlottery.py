import random

# Assigning numbers to each team based on their percentages in reverse order
team_assignments = {
    "Britt": list(range(190, 250)),
    "Mike": list(range(150, 190)),
    "Nick": list(range(120, 150)),
    "Jack": list(range(90, 120)),
    "Carl": list(range(60, 90)),
    "Brian": list(range(40, 60)),
    "Muneer": list(range(20, 40)),
    "Scott": list(range(10, 20)),
    "Steve": list(range(5, 10)),
    "Tony": list(range(1, 5))
}

# Initialize an empty list to store the draft order
draft_order = []

# Continue until all teams are assigned to a draft slot
while team_assignments:
    # Pick a random number from 1 to 100
    random_number = random.randint(1, 250)
    
    # Find the team associated with the random number
    for team, numbers in team_assignments.items():
        if random_number in numbers:
            # Add the winning team to the draft order
            draft_order.append(team)
            
            # Remove the winning team's range from the list of teams
            del team_assignments[team]
            
            break

# Print the final draft order
print("Final draft order:")
for i, team in enumerate(draft_order):
    print(f"{i + 1}. {team}")
