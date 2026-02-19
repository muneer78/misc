import random


def weighted_draft_selection(teams, weights, num_picks, min_pick_for_team1=5):
    """
    Perform weighted draft selection.

    Args:
        teams: List of team names
        weights: List of weights (probabilities) for each team
        num_picks: Number of picks to make
        min_pick_for_team1: Team 1 must be selected by this pick (1-indexed)
    """
    picks = []
    remaining_teams = teams.copy()
    remaining_weights = weights.copy()

    for pick_num in range(1, num_picks + 1):
        # Normalize weights to sum to 1
        total_weight = sum(remaining_weights)
        normalized_weights = [w / total_weight for w in remaining_weights]

        # If we're at the last chance for Team 1 and it hasn't been picked
        if pick_num == min_pick_for_team1 and "Team 1" in remaining_teams:
            selected = "Team 1"
        else:
            selected = random.choices(remaining_teams, weights=normalized_weights, k=1)[0]

        picks.append(selected)
        print(f"Pick {pick_num}: {selected}")

        # Remove selected team
        idx = remaining_teams.index(selected)
        remaining_teams.pop(idx)
        remaining_weights.pop(idx)

    return picks


teams = ["Team 1", "Team 2", "Team 3", "Team 4", "Team 5",
         "Team 6", "Team 7", "Team 8", "Team 9", "Team 10"]
weights = [15.0, 15.0, 15.0, 13.5, 11.5, 9.0, 7.5, 6.0, 4.5, 3.0]

picks = weighted_draft_selection(teams, weights, num_picks=10, min_pick_for_team1=5)
print("\nFinal Draft Order:")
for i, team in enumerate(picks, 1):
    print(f"{i}. {team}")