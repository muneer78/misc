# Input string with line breaks
input_string <- "a\nb\ngc\nd\ne\ng\nh\ni"

# Split the string into a list, removing leading/trailing whitespaces
strings_list <- strsplit(input_string, "\n")[[1]]  # [[1]] to extract the vector

# Separate each string with a comma
result <- paste(strings_list, collapse = ", ")

# Print the result
cat(result, "\n")  # Use cat for printing with a newline
