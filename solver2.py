from pulp import LpProblem, LpMaximize, LpVariable, LpStatus

# Create a linear programming problem
prob = LpProblem("Maximize_Items", LpMaximize)

# Define variables: number of items of each type to buy
item_1 = LpVariable("Coffee", lowBound=0, cat="Integer")
item_2 = LpVariable("Mello Yello Zero", lowBound=0, cat="Integer")

# Define prices and budget
prices = [1.08, 3.27]
budget = 7.35

# Define the individual objectives for each item
objective_item_1 = item_1
objective_item_2 = item_2

# Define the constraint: total cost should not exceed the budget
prob += prices[0] * item_1 + prices[1] * item_2 <= budget, "Budget_Constraint"

# Add constraints to purchase at least one unit of Mello Yello Zero and at least 2 units of Coffee
prob += item_2 >= 1, "At_Least_One_Item2"
prob += item_1 >= 2, "At_Least_Two_Item1"

# Define the weighted sum of objectives
total_objective = 0.2 * objective_item_1 + 1.1 * objective_item_2

# Set the objective to maximize the total_objective
prob += total_objective

# Solve the problem
prob.solve()

# Calculate the total cost of the purchased items
total_cost = prices[0] * item_1.varValue + prices[1] * item_2.varValue

# Calculate the remaining budget
remaining_budget = budget - total_cost
remaining_budget_rounded = round(remaining_budget, 2)

# Print the results
print("Status:", LpStatus[prob.status])
print("Coffee:", item_1.varValue)
print("Mello Yello Zero:", item_2.varValue)
print("Total items:", item_1.varValue + item_2.varValue)
print("Remaining budget:", remaining_budget_rounded)