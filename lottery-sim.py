import numpy as np
import pandas as pd

# Initialize size and simulate outcome

np.random.seed(111)
lottery_ticket_cost, num_tickets, grand_prize = 5, 1000000, 1000000
chance_of_winning = 1/num_tickets
size = 2000000
payoffs = [-lottery_ticket_cost, grand_prize-lottery_ticket_cost]
probs = [1-chance_of_winning, chance_of_winning]
outcomes = np.random.choice(a=payoffs, size=size, p=probs, replace=True)
# Mean of Outcomes
answer=outcomes.mean()
print("Average payoff from {} simulations = {}".format(size, answer))

# Initialize simulations and cost of ticket
np.random.seed(111)
sims, lottery_ticket_cost = 2000000, 0
# Use a while loop to increment `lottery_ticket_cost` till average value of outcomes falls below zero
while 1:
    outcomes = np.random.choice([-lottery_ticket_cost, grand_prize-lottery_ticket_cost],
                 size=sims, p=[1-chance_of_winning, chance_of_winning], replace=True)
    if outcomes.mean() < 0:
        break
    else:
        lottery_ticket_cost += 1
answer = lottery_ticket_cost - 1
print("As the average expected payoff is negative. The highest price at which it makes sense to buy the ticket is {}".format(answer))