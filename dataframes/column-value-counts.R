if (!require("data.table")) install.packages("data.table")
library(data.table)
if (!require("tidyverse")) install.packages("tidyverse")
library(tidyverse)

library(data.table)
library(tidyverse)  

# Function to load data
load_data <- function(file_path) {
  fread(file_path)
}

# Function to count occurrences of 'exit' in each column
count_exit_in_column <- function(df) {
  sapply(df, function(column) sum(grepl("exit", tolower(column))))
}

# Function to calculate differences in counts between old and new datasets
calculate_differences <- function(counts1, counts2, columns) {
  differences <- counts2 - counts1
  names(differences) <- columns
  differences[is.na(differences)] <- 0  # Replace NA with 0 for columns not present in counts1
  differences
}

# Function to print results
print_results <- function(total_rows, counts, title) {
  cat(paste("Total rows:", total_rows, "\n"))
  cat(paste(title, ":\n"))
  for (column in names(counts)) {
    cat(paste(column, ":", counts[[column]], "\n"))
  }
  cat("\n")
}

# Function to print differences
print_differences <- function(differences, sorted_columns_diff) {
  cat("Difference in counts in old vs new dataset:\n")
  for (column in sorted_columns_diff) {
    cat(paste(column, ":", differences[[column]], "\n"))
  }
}

# Load datasets
df1 <- load_data('cadence_20240503_182156000.csv')
df2 <- load_data('CadenceSalesforceActiveInactiveCriteria.csv')

# Count total rows in each DataFrame
total_rows_df1 <- nrow(df1)
total_rows_df2 <- nrow(df2)

# Count occurrences of 'exit' in each column
count_df1 <- count_exit_in_column(df1)
count_df2 <- count_exit_in_column(df2)

# Calculate differences in counts between old and new datasets
differences <- calculate_differences(count_df1, count_df2, names(df1))

# Sort columns by the differences in counts
sorted_columns_diff <- names(differences)[order(differences)]

# Print results
print_results(total_rows_df1, count_df1, "Sorted column order by number of 'exit' occurrences in old dataset")
print_results(total_rows_df2, count_df2, "Sorted column order by number of 'exit' occurrences in new dataset")
print_differences(differences, sorted_columns_diff)
