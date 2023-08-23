from pulp import LpProblem, LpMaximize, LpVariable, LpStatus

# Create a linear programming problem
prob = LpProblem("Maximize_Items", LpMaximize)

# Define variables: number of items of each type to buy
item_1 = LpVariable("Coffee", lowBound=0, cat="Integer")
item_2 = LpVariable("Breakfast", lowBound=0, cat="Integer")
item_3 = LpVariable("Sports Betting", lowBound=0, cat="Integer")

# Define prices and budget
prices = [1.08, 3.26, 5]
budget = 75

# Define the objective function: maximize the total number of items
prob += item_1 + item_2 + item_3, "Total_Items"

# Define the constraint: total cost should not exceed the budget
prob += prices[0] * item_1 + prices[1] * item_2 + prices[2] * item_3 <= budget, "Budget_Constraint"

# Add constraints to purchase at least one unit of Item 3 and at least 4 units of Item 2
prob += item_3 >= 1, "At_Least_One_Item3"
prob += item_2 >= 4, "At_Least_Four_Item2"

# Solve the problem
prob.solve()

# Calculate the total cost of the purchased items
total_cost = prices[0] * item_1.varValue + prices[1] * item_2.varValue + prices[2] * item_3.varValue

# Calculate the remaining budget
remaining_budget = budget - total_cost

# Print the results
print("Status:", LpStatus[prob.status])
print("Coffee:", item_1.varValue)
print("Breakfast:", item_2.varValue)
print("Sports Betting:", item_3.varValue)
print("Total items:", item_1.varValue + item_2.varValue + item_3.varValue)
print("Remaining budget:", remaining_budget)
