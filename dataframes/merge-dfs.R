# Install and load the tidyverse package
if (!requireNamespace("tidyverse", quietly = TRUE)) {
  install.packages("tidyverse")
}
library(tidyverse)

# Read CSV files into DataFrames
df1 <- read_csv('cadence_20240503_182156000.csv')
df2 <- read_csv('CadenceSalesforceActiveInactiveCriteria.csv')

file <- 'cadence'

# Get the filename without extension
filename <- tools::file_path_sans_ext(basename(file))

# Perform an inner join on the two DataFrames
result <- inner_join(df1, df2, by = c("factorsoft_client_number__c" = "clientno"))

# Save the DataFrame with unique records to a new CSV file
write_csv(result, paste0(filename, '-merged.csv'))

# Print the result as a tibble
print(result)