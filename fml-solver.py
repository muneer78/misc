from scipy.optimize import linprog

# Define prices and projected profits
prices = [422, 235, 221, 200, 188, 155, 89, 32, 21]
profits = [122, 120, 95, 78, 65, 45, 25, 10, 3]
budget = 1000
penalty_cost = -20  # Penalty for each unused slot

# Define coefficients of the objective function to maximize
c = [-profits[i] for i in range(len(prices))] + [penalty_cost] * len(prices)

# Define coefficients of the inequality constraints (left-hand side)
A = [prices[i] for i in range(len(prices))]

# Right-hand side values of the inequality constraints
b = [budget]

# Bounds for the decision variables
bounds = [(0, None) for _ in range(len(prices))] + [(0, 1) for _ in range(len(prices))]

# Constraint: Total items purchased should be exactly 10
A_total_items = [1 for _ in range(len(prices))]
b_total_items = 10

# Combine constraints
A_combined = [A + [0] * len(prices), A_total_items + [0] * len(prices)]
b_combined = b + [b_total_items]

# Solve the linear programming problem
result = linprog(c, A_ub=A_combined, b_ub=b_combined, bounds=bounds, method="highs")

# Calculate the count of unused slots
unused_slots = b_total_items - int(sum(result.x[: len(prices)]))

# Calculate the total projected profit before adding the penalty cost
total_projected_profit_before_penalty = -result.fun

# Calculate the total projected profit after adding the penalty cost
total_projected_profit_after_penalty = total_projected_profit_before_penalty + (
    penalty_cost * unused_slots
)

# Print the results
if result.success:
    print("Status: Success")
    for i, item in enumerate(result.x[: len(prices)]):
        print(f"Movie{i + 1}: {int(item)}")
    print("Unused slots:", unused_slots)
    print("Total items:", b_total_items - unused_slots)
    print(
        "Total projected profit before penalty:",
        round(total_projected_profit_before_penalty, 2),
    )
    print(
        "Total projected profit after penalty:",
        round(total_projected_profit_after_penalty, 2),
    )
    print(
        "Remaining budget:",
        round(budget - sum(prices[i] * result.x[i] for i in range(len(prices))), 2),
    )
else:
    print("Status: Failed to find a solution")
