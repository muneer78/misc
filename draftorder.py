"""
Use numpy to shuffle items
"""
import numpy as np

places = ["10th", "9th", "8th", "7th", "6th", "5th", "4th", "3rd", "2nd", "1st"]
np.random.shuffle(places)
print(places)
