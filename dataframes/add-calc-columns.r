# Load necessary libraries
if (!require("dplyr")) install.packages("dplyr")
if (!require("readr")) install.packages("readr")
if (!require("stringr")) install.packages("stringr")

library(dplyr)
library(readr)
library(stringr)

# Read the CSV file into a DataFrame
df <- read_csv("C:/Users/mahmad/OneDrive - Ryan RTS/Downloads/large_files.csv")

# Convert the Size column values from bytes to MB and write to a new column called size_in_mb
df <- df %>%
  mutate(size_in_mb = round(Size / (1024 * 1024), 2))

# Update all headers to lowercase and replace whitespace with dashes
colnames(df) <- colnames(df) %>%
  tolower() %>%
  str_replace_all(" ", "-")

# Sort the DataFrame by size_in_mb in descending order
df_sorted <- df %>%
  arrange(desc(size_in_mb))

# Write the updated DataFrame to a new CSV file
output_file <- "C:/Users/mahmad/OneDrive - Ryan RTS/Downloads/large-files-final.csv"
write_csv(df_sorted, output_file)

cat("Output done\n")