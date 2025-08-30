if (!require("dplyr")) install.packages("dplyr")
if (!require("readxl")) install.packages("readxl")

# Load necessary libraries
library(dplyr)
library(readxl)

# Read the Excel file
url <- "https://github.com/chris1610/pbpython/raw/master/data/sample-sales-reps.xlsx"
temp_file <- tempfile(fileext = ".xlsx")
download.file(url, temp_file, mode = "wb")
df <- read_excel(temp_file)

# Add a default commission column
df <- df %>%
  mutate(commission = 0.02)

# Update commission for specific conditions
df <- df %>%
  mutate(
    commission = ifelse(category == "Shirt", 0.025, commission),
    commission = ifelse(category == "Belt" & quantity >= 10, 0.04, commission)
  )

# Add a bonus column
df <- df %>%
  mutate(bonus = 0)

# Update bonus and commission for specific conditions
df <- df %>%
  mutate(
    bonus = ifelse(category == "Shoes" & `ext price` >= 1000, 250, bonus),
    commission = ifelse(category == "Shoes" & `ext price` >= 1000, 0.045, commission)
  )

# Calculate the compensation for each row
df <- df %>%
  mutate(comp = commission * `ext price` + bonus)

# Summarize and round the results by sales rep
summary <- df %>%
  group_by(`sales rep`) %>%
  summarize(total_comp = round(sum(comp), 2))

# Print the summary
print(summary)