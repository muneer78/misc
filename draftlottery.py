import random

# Assigning numbers to each team based on their percentages in reverse order
team_assignments = {
    "Britt": list(range(91, 101)),
    "Mike": list(range(81, 91)),
    "Nick": list(range(71, 81)),
    "Jack": list(range(59, 71)),
    "Carl": list(range(46, 59)),
    "Brian": list(range(36, 46)),
    "Muneer": list(range(26, 36)),
    "Scott": list(range(15, 26)),
    "Steve": list(range(5, 15)),
    "Tony": list(range(1, 5))
}

# Initialize an empty list to store the draft order
draft_order = []

# Continue until all teams are assigned to a draft slot
while team_assignments:
    # Pick a random number from 1 to 100
    random_number = random.randint(1, 100)
    
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
