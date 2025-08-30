# Install required package if not already installed
library(lpSolve)

# Create the linear program object
prob <- lp.model(control = list(show.all = FALSE))  # Suppress verbose output

# Define objective function (maximize)
objective <- c(0.2, 1.1)  # Weights for each item

# Define variables with integer constraints
item_1 <- lp.variable(prob, name = "Coffee", cat = "integer")
item_2 <- lp.variable(prob, name = "Mello_Yello_Zero", cat = "integer")

# Define costs of each item
costs <- c(1.08, 3.27)

# Budget constraint
lp.addConstraint(prob, costs[1] * item_1 + costs[2] * item_2 <= 7.35, "Budget_Constraint")

# Minimum purchase constraints
lp.addConstraint(prob, item_2 >= 1, "At_Least_One_Item2")
lp.addConstraint(prob, item_1 >= 2, "At_Least_Two_Item1")

# Set objective function to maximize weighted sum
lp.setObjective(prob, objective %*% c(item_1, item_2), maximize = TRUE)

# Solve the problem
lp.solve(prob)

# Extract solution values
coffee_purchased <- lp.solution(prob, item_1)
mello_yello_purchased <- lp.solution(prob, item_2)
total_items <- coffee_purchased + mello_yello_purchased

# Calculate total cost and remaining budget
total_cost <- costs[1] * coffee_purchased + costs[2] * mello_yello_purchased
remaining_budget <- 7.35 - total_cost

# Print results
cat("Status:", lp.getStatus(prob), "\n")
cat("Coffee:", coffee_purchased, "\n")
cat("Mello Yello Zero:", mello_yello_purchased, "\n")
cat("Total items:", total_items, "\n")
cat("Remaining budget:", round(remaining_budget, 2), "\n")

