if (!require("data.table")) install.packages("data.table")
library(data.table)
if (!require("tidyverse")) install.packages("tidyverse")
library(tidyverse)

# Load the CSV files into DataFrames
df1 <- read_csv('A_only.csv')
df2 <- read_csv('B_only.csv')

# Filter df1
# df1 <- df1 %>% filter(str_detect(nk_fuelcardid, "347907"))
df1 <- grepl("347907", df1$nk_fuelcardid)

# Calculate the max value of col in dataset 1
max_col1_df1 <- max(df1$totalfuelamt)

# Filter df2
df2 <- df2 %>% filter(str_detect(`Carrier Id`, '347907'))

# Calculate the max value of col in dataset 2
max_col1_df1 <- max(df1_filtered$totalfuelamt, na.rm = TRUE)

# Calculate the difference
difference <- max_col1_df1 - max_col1_df2

# Write all calculations to console
cat("Max value of col1 in dataset 1:", max_col1_df1, "\n")
cat("Max value of col1 in dataset 2:", max_col1_df2, "\n")
cat("Difference between max values:", difference, "\n")