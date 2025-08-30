# Install and load necessary packages
if (!require("tidyverse")) install.packages("tidyverse")
library("tidyverse")

# Define the file path
file <- 'fieldmapping_processed.csv'

# Get the filename without extension
filename <- tools::file_path_sans_ext(basename(file))

# Read the CSV file into a DataFrame
dforig <- read_csv(file)

# Drop duplicates based on "int_field" and "ext_field"
df <- dforig %>% distinct(int_field, ext_field, .keep_all = TRUE)

# Save the DataFrame with unique records to a new CSV file
write_csv(df, paste0(filename, 'uniques.csv'))

print('Done')