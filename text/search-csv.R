# This code optimizes searching for a few records in a large dataset.

if (!require("tidyverse")) install.packages("tidyverse")
library(tidyverse)
if (!require("data.table")) install.packages("data.table")
library(data.table)

# Read the CSV file into a data frame
df_alldata <- read.csv("futures.csv")

# Define the search items as a character vector and convert to uppercase
search_items <- toupper(c("royals", "heat"))

# **Ensure the column name for filtering exists**
column_to_filter <- "Pick"  # Replace with the actual column name in your data

# Check if the column exists
if (!all(column_to_filter %in% names(df_alldata))) {
  stop("Error: Column name for filtering not found. Check your data.")
}

# Convert the column values to uppercase for case-insensitive search
df_alldata <- df_alldata %>%
  mutate({{column_to_filter}} := toupper({{column_to_filter}}))

# Filter rows where 'column_to_filter' contains any search term (case-insensitive)
filtered_data <- df_alldata %>%
  filter(grepl(paste(search_items, collapse="|"), {{column_to_filter}}), ignore.case = TRUE)

# Print the filtered data
print(filtered_data)