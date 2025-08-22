from random import choice


def get_winning_ticket(possibilities):
    winning_ticket = []

    # pulling a number out of the list until 4 have been pulled

    while len(winning_ticket) < 4:
        pulled_item = choice(possibilities)

        # adding the number to the ticket

        if pulled_item not in winning_ticket:
            winning_ticket.append(pulled_item)

    return winning_ticket


def get_your_ticket(possibilities):
    your_ticket = []

    while len(your_ticket) < 4:
        pulled_item = choice(possibilities)

        if pulled_item not in winning_ticket:
            your_ticket.append(pulled_item)
    return your_ticket


def checking_ticket(played_ticket, winning_ticket):
    for element in played_ticket:
        if element not in winning_ticket:
            return False

    return True


possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "a", "b", "c", "d", "e"]
winning_ticket = get_winning_ticket(possibilities)

won = False
plays = 0

max_tries = 10000000

while not won:
    new_ticket = get_your_ticket(possibilities)
    won = checking_ticket(new_ticket, winning_ticket)
    plays += 1
    if plays >= max_tries:
        break

if won:
    print("We have a winning ticket!")
    print(f"Your ticket: {new_ticket}")
    print(f"Winning ticket: {winning_ticket}")
    print(f"It only took {plays} tries to win!")
else:
    print(f"Tried {plays} times, without pulling a winner. :(")
    print(f"Your ticket: {new_ticket}")
    print(f"Winning ticket: {winning_ticket}")
