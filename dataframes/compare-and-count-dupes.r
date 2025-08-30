if (!require("dplyr")) install.packages("dplyr")
if (!require("readr")) install.packages("readr")
if (!require("openxlsx")) install.packages("openxlsx")

# Load necessary libraries
library(dplyr)
library(readr)
library(openxlsx)

# Read the CSV files
df1 <- read_csv("DS4220-20240517.csv")
df2 <- read_csv("TransactionSummaryLLCGrp_Daily_184835_05-09-2024v2.csv")

# Total records in each data frame
df1_len <- nrow(df1)
df2_len <- nrow(df2)

cat("Count of records in df1:", df1_len, "\n")
cat("Count of records in df2:", df2_len, "\n")

# Count duplicate values in transaction ID columns
df1_transid_dupes <- nrow(df1) - nrow(distinct(df1, transid))
df2_transid_dupes <- nrow(df2) - nrow(distinct(df2, `Trans. Id`))

cat("Number of duplicate transaction IDs in df1:", df1_transid_dupes, "\n")
cat("Number of duplicate transaction IDs in df2:", df2_transid_dupes, "\n")

# Count of records that are in df1 but not in df2
df1_not_in_df2 <- df1 %>%
  filter(!(transid %in% df2$`Trans. Id`)) %>%
  distinct()
df1_not_in_df2_count <- nrow(df1_not_in_df2)

# Count of records that are in df2 but not in df1
df2_not_in_df1 <- df2 %>%
  filter(!(`Trans. Id` %in% df1$transid)) %>%
  distinct()
df2_not_in_df1_count <- nrow(df2_not_in_df1)

cat("Count of records in df1 but not in df2:", df1_not_in_df2_count, "\n")
cat("Count of records in df2 but not in df1:", df2_not_in_df1_count, "\n")

# Export the differences to an Excel file
date <- format(Sys.Date(), "%Y-%m-%d")
excel_file_name <- paste0(date, "-Diff.xlsx")

write.xlsx(list(
  DF1NotInDF2 = df1_not_in_df2,
  DF2NotInDF1 = df2_not_in_df1
), file = excel_file_name)

cat("Differences exported to", excel_file_name, "\n")