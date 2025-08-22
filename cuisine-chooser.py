"""
Using random to generate list
"""

import random

cuisine_type = [
    "Indian",
    "Salvadoran",
    "Mediterranean",
    "Deli",
    "Mexican",
    "Chinese",
    "Thai",
    "Italian",
    "BBQ",
    "Japanese",
    "Korean",
    "Greek",
    "Food Hall",
]
output_type = random.sample(cuisine_type, k=3)
MESSAGE = "Your cuisine choice is: "

print(MESSAGE + ", ".join(output_type))
