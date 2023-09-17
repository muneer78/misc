import random

def trial() :
    sequence = [ ]
    # dist =  [0.140,0.140,0.140,0.125,0.105,0.090,0.075,0.060,0.045,0.030,0.020,0.015,0.010,0.005]
    dist = [ 114 , 113 , 112 , 111 , 99 , 89 , 79 , 69 , 59 , 49 , 39 , 29 , 19 , 9 , 6 , 4 ]
    pool = [ idx + 1 for idx , elem in enumerate ( dist ) ]
    # for i in range(4):
    for i in range ( 5 ) :
        selected = random.choices ( population = pool , weights = dist ) [ 0 ]
        sequence.append ( selected )
        idx = pool.index ( selected )
        del pool [ idx ]
        del dist [ idx ]
    sequence.extend ( pool )
    return sequence


import numpy as np

np.set_printoptions ( linewidth = 150 , precision = 4 , suppress = True )
from collections import Counter


def simulate(rounds=1000) :
    trial_runs = [ ]
    for i in range ( rounds ) :
        trial_runs.append ( trial () )

    arrays = [ ]
    # for j in range(14):
    for j in range ( 16 ) :
        count = Counter ( [ t [ j ] for t in trial_runs ] )
        count = {k : v / rounds for k , v in count.items ()}
        # count = [round(count[i],3) if i in count else 0 for i in range(1,15)]
        count = [ round ( count [ i ] , 3 ) if i in count else 0 for i in range ( 1 , 17 ) ]
        arrays.append ( count )

    arr = np.array ( arrays )
    return arr.transpose ()


simulate ( rounds = 5000000 )