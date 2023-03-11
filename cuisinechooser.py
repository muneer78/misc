import random

type = ["Indian", "Salvadoran", "Mediterranean", "Deli", "Mexican", "Chinese", "Thai", "Italian", "BBQ", "Japanese", "Korean", "Greek", "Food Hall"]
output_type = random.sample(type, k=3)
message = 'Your cuisine choice is: '

print(message + ', '.join(output_type))