# Load necessary libraries
library(dplyr)
library(readr)

# Read the dataset from a CSV file
df <- read_csv("C:/Users/mahmad/OneDrive - Ryan RTS/Downloads/algo.csv")

# Add a new column that contains the sum of all numeric columns for each row
df <- df %>%
  rowwise() %>%
  mutate(total = round(sum(c_across(where(is.numeric))), 1)) %>%
  ungroup()

# Save the modified DataFrame to a new CSV file
output_file <- "C:/Users/mahmad/OneDrive - Ryan RTS/Downloads/algo_filtered.csv"
write_csv(df, output_file)

cat("Job done\n")