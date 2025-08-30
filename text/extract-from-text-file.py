# Define the path to the text file
text_file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\code\parameters.txt"

# Define the path to the output file
output_file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\extracted_names.txt"

# Read the text file and extract lines containing 'silver.hubtek'
with open(text_file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

extracted_lines = [line for line in lines if "silver.hubtek" in line]

# Save the extracted lines to a new text file
with open(output_file_path, "w", encoding="utf-8") as file:
    file.writelines(extracted_lines)

print(f"Extracted lines saved to {output_file_path}")
