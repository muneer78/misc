import random

num_games = 1000
win_count = 0
doors = [1, 2, 3]

for i in range(num_games):
    car = random.choice(doors)
    first_pick = random.choice(doors)

    host_can_open = set(doors) - set([car, first_pick])
    host_opens = random.choice(list(host_can_open))

    second_pick = min(set(doors) - set([first_pick, host_opens]))

    if second_pick == car:
        win_count += 1

    if i < 5:
        print(f"{first_pick=}, {host_opens=}, {second_pick=}, {car=}")

print(f"\nWin percentage from always switching: {win_count / num_games:.1%}")
