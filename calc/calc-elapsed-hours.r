# Load necessary library
if (!require("lubridate")) install.packages("lubridate")

library(lubridate)

# Function to calculate hours elapsed
calculate_hours_elapsed <- function(input_time_str) {
  # Get the current time
  current_time <- now()
  
  # Parse the input time
  input_time <- ymd_hms(input_time_str)
  
  # Calculate the number of hours elapsed
  elapsed_time <- as.numeric(difftime(current_time, input_time, units = "hours"))
  
  return(elapsed_time)
}

# Example usage
input_time_str <- "2025-01-03 15:00:00"
elapsed_hours <- calculate_hours_elapsed(input_time_str)
cat(sprintf("Number of hours elapsed: %.2f\n", elapsed_hours))