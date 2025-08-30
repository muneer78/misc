# Install and load necessary packages
if (!require("tidyverse")) install.packages("tidyverse")
library("tidyverse")

if (!require("glue")) install.packages("glue")
library(glue)

# Load the data
df1 <- read_csv('cadence_20240503_182156000.csv')
df2 <- read_csv('CadenceSalesforceActiveInactiveCriteria.csv')

# Ensure column names are consistent by removing "__c" from both df1 and df2
df1 <- df1 %>% rename_with(~str_replace_all(., "__c", ""))
df2 <- df2 %>% rename_with(~str_replace_all(., "__c", ""))

# Remove duplicates
df1_unique <- df1 %>% distinct()
df2_unique <- df2 %>% distinct()

# Define the columns to compare
col_df1 <- "factorsoft_client_number"
col_df2 <- "masterclientno"

# Convert strings to symbols
col_sym_df1 <- sym(col_df1)
col_sym_df2 <- sym(col_df2)

# Count of records that are in df1 but not df2
df1_not_in_df2 <- df1_unique %>%
  filter(!(eval(col_sym_df1, df1_unique) %in% eval(col_sym_df2, df2_unique)))
df1_not_in_df2_count <- nrow(df1_not_in_df2)

# Count of records that are in df2 but not df1
df2_not_in_df1 <- df2_unique %>%
  filter(!(eval(col_sym_df2, df2_unique) %in% eval(col_sym_df1, df1_unique)))
df2_not_in_df1_count <- nrow(df2_not_in_df1)

# Print the counts
print(glue("Count of records in df1 but not df2: {df1_not_in_df2_count}"))
print(glue("Count of records in df2 but not df1: {df2_not_in_df1_count}"))