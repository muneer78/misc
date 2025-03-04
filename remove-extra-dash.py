import os

def remove_extra_dash(directory):
    for filename in os.listdir(directory):
        if "--" in filename:
            new_filename = filename.replace("--", "-", 1)  # Replace first occurrence of "--"
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f'Renamed: {filename} -> {new_filename}')

# Specify the directory
directory = '/Users/muneer78/Downloads/videos'
remove_extra_dash(directory)
