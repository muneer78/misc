from itertools import permutations

paths = permutations([1, 2, 3])  # Generate all permutations of the list [1, 2, 3]
for path in paths:
    print(path)
