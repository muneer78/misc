import os

def search_in_files(search_string, directory):
    found_files = []
    files_searched = 0
    for file_name in os.listdir(directory):
        if file_name.__contains__('.md'):
            files_searched += 1
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if search_string in line:
                        found_files.append(file_path)
                        break  # Stop searching this file once the string is found
    return found_files, files_searched

# Example usage:
search_string = input("Enter the string to search for: ")
directory = input("Enter the directory to search in: ")

found_files, files_searched = search_in_files(search_string, directory)
if found_files:
    print("Found in these files:")
    for file_path in found_files:
        print(file_path)
else:
    print("String not found in any files.")
print("Total files searched:", files_searched)