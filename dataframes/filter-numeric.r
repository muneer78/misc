if (!require("dplyr")) install.packages("dplyr")

# Load necessary library
library(dplyr)

# Read the CSV file
df <- read.csv("C:/Users/mahmad/OneDrive - Ryan RTS/Downloads/pointdist25.csv")

# Filter out rows where the 'Rank' column has a value of 1, 2, or 3
filtered_df <- df %>% filter(!(Rank %in% c(1, 2, 3)))

# Save the updated DataFrame to a new CSV file
output_file_path <- "C:/Users/mahmad/OneDrive - Ryan RTS/Downloads/pointdist25-filtered.csv"
write.csv(filtered_df, output_file_path, row.names = FALSE)

cat(sprintf("Filtered DataFrame saved to %s\n", output_file_path))