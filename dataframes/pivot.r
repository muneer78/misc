if (!require("tidyverse")) install.packages("tidyverse")
if (!require("glue")) install.packages("glue")

# Load necessary libraries, install if not available
if (!require("tidyverse")) install.packages("tidyverse")
if (!require("glue")) install.packages("glue")

# Load libraries
library(tidyverse)
library(glue)

# Function to generate summary table
generate_summary_table <- function(df, group_column) {
  summary_table <- df %>%
    group_by(!!sym(group_column)) %>%
    summarize(row_count = n())
  return(summary_table)
}

# Read the CSV file
df <- read_csv("C:/Users/mahmad/OneDrive - Ryan RTS/Downloads/20250310-PasswordChange(ms_pwl_sorted).csv")

# Define the column to group by
group_column <- "Risk Level"  # Replace with the actual column name to group by

# Generate summary table
summary_table <- generate_summary_table(df, group_column)

name <- "password"
date <- Sys.Date()

# Print and export summary table
print(summary_table)

path <- glue("C:/Users/mahmad/OneDrive - Ryan RTS/Downloads/{date}_{name}_pivot.csv")

write_csv(summary_table, path)