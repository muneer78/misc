import os

def compare_files(file1_name, file2_name):
    # Get the current directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct full file paths
    file1_path = os.path.join(script_dir, file1_name)
    file2_path = os.path.join(script_dir, file2_name)
    
    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()

            # Compare line by line
            for i, line2 in enumerate(lines2):
                if i < len(lines1) and line2 != lines1[i]:
                    print(f"Difference found at line {i + 1}:")
                    print(f"String 1: {lines1[i].strip()}")
                    print(f"String 2: {line2.strip()}\n")

            # Check if any additional lines exist in file2
            if len(lines2) > len(lines1):
                for j in range(len(lines1), len(lines2)):
                    print(f"Additional line in String 2 (line {j + 1}): {lines2[j].strip()}")

            if lines1 == lines2:
                print("Identical")
    except FileNotFoundError:
        print("Error: One or both files not found.")

# Usage
compare_files("string1.txt", "string2.txt")
