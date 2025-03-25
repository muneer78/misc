import random

def selectWinners(allEntries, numWinners):
    winners = []
    print("Selecting %d winners" % numWinners)
    print("Entries", allEntries)
    for i in range(numWinners):
        winner = random.choice(allEntries)
        print("%d: %s won" % (i+1, winner))
        allEntries[:] = [x for x in allEntries if x != winner]

entrants = ['10th', '9th', '8th', '7th', '6th', '5th', '4th', '3rd', '2nd', '1st']
allEntries = []
for entrant in entrants:
    numEntries = random.randint(1, 5)
    print("%s has %d entries" % (entrant, numEntries))
    allEntries.extend([entrant] * numEntries)
selectWinners(allEntries, 10)