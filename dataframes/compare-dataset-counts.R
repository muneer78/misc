# Load necessary library
if (!require("data.table")) install.packages("data.table")
library(data.table)
if (!require("tidyverse")) install.packages("tidyverse")
library(tidyverse)

# Load the CSV files using data.table
df1 <- fread('A_only.csv')
df2 <- fread('B_only.csv')

# Count the number of records in each dataframe
count_df1 <- nrow(df1)
count_df2 <- nrow(df2)

# Check if the counts are calculated correctly
if (!is.null(count_df1) && !is.null(count_df2)) {
  # Calculate the difference in counts
  difference <- count_df1 - count_df2
  
  # Print the counts and the difference
  cat('Count of dataset 1:', count_df1, '\n')
  cat('Count of dataset 2:', count_df2, '\n')
  cat('Difference in counts:', difference, '\n')
} else {
  cat('Error in calculating the counts.\n')
}
