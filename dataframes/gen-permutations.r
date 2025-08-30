if (!require("gtools")) install.packages("gtools")

# Load necessary library
library(gtools)

# Generate all permutations of the list c(1, 2, 3)
paths <- permutations(n = 3, r = 3, v = c(1, 2, 3))

# Print each permutation
apply(paths, 1, function(path) {
  print(path)
})