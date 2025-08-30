import random

# ------
# CONFIG
# ------
stop_on_jackpot = True
powerplay = True
reset_max = True
print_every = 10000000  # changed to tickets purchased, rather than spent $$$
jackpot_value = 1300000000
# ------

prizes = {
    (0, False): 0,
    (1, False): 0,
    (2, False): 0,
    (3, False): 7,
    (4, False): 100,
    (5, False): 1000000,
    (0, True): 4,
    (1, True): 4,
    (2, True): 7,
    (3, True): 100,
    (4, True): 50000,
    (5, True): jackpot_value,
}

ticket_numbers = set(range(5))
ticket_powerball = 0

balls = tuple(range(69))
powerballs = tuple(range(26))

winnings = 0
spent = 0
max_prize = 0
jackpot = False
powerplay_draw = 0
powerplay_multiplier = 0
iterations = 0

while not jackpot or not stop_on_jackpot:
    chosen_balls = random.sample(balls, 5)
    chosen_powerball = random.choice(powerballs)

    numbers_hit = sum(1 for x in chosen_balls if x in ticket_numbers)
    powerball_hit = chosen_powerball == ticket_powerball
    matches = (numbers_hit, powerball_hit)
    jackpot = matches == (5, True)

    if powerplay:
        if jackpot_value > 150000000:
            powerplay_draw = random.randint(1, 42)
        else:
            powerplay_draw = random.randint(1, 43)

        if powerplay_draw <= 24:
            powerplay_multiplier = 2
        elif powerplay_draw <= 24 + 13:
            powerplay_multiplier = 3
        elif powerplay_draw <= 24 + 13 + 3:
            powerplay_multiplier = 4
        elif powerplay_draw <= 24 + 13 + 3 + 2:
            powerplay_multiplier = 5
        else:
            powerplay_multiplier = 10

        if jackpot:
            powerplay_multiplier = 1
        elif matches == (5, False):
            powerplay_multiplier = 2

        spent += 3
    else:
        powerplay_multiplier = 1
        spent += 2

    prize = prizes[matches] * powerplay_multiplier
    winnings += prize
    max_prize = max(prize, max_prize)
    iterations += 1

    if iterations % print_every == 0 or jackpot:
        stats = "spent:{:,}, winnings:{:,}, net:{:,} max_win:{:,}".format(
            spent, winnings, winnings - spent, max_prize
        )
        print(stats)
        if reset_max:
            max_prize = 0
