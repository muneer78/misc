# List of cuisine types
cuisine_type <- c("Indian", "Salvadoran", "Mediterranean", "Deli", 
                  "Mexican", "Chinese", "Thai", "Italian", "BBQ", 
                  "Japanese", "Korean", "Greek", "Food Hall")

# Generate random sample of 3 cuisines
output_type <- sample(cuisine_type, size = 3)

# Message
message <- "Your cuisine choice is: "

# Combine message and list elements with comma separation
result <- paste(message, paste(output_type, collapse = ", "), sep = "")

# Print the result
cat(result, "\n")
