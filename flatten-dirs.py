import os
import shutil

# Specify the master directory
master_dir = '/Users/muneer78/'  # Change this to your target master directory

# Loop through files in the master directory and its subdirectories
for root, _, files in os.walk(master_dir):
    # Check if the current directory is two levels below the master directory
    rel_path = os.path.relpath(root, master_dir)
    if rel_path.count(os.sep) == 2:  # Two levels deep
        
        for f in files:
            source_path = os.path.join(root, f)
            
            # Get the directory path two levels below to move the file
            two_level_below_dir = os.path.join(master_dir, os.path.split(root)[0])
            
            # Create the destination directory if it doesn't exist
            if not os.path.exists(two_level_below_dir):
                os.makedirs(two_level_below_dir)
            
            # Move the file to this directory
            destination_path = os.path.join(two_level_below_dir, f)
            shutil.move(source_path, destination_path)
            print(f"Moved: {source_path} -> {destination_path}")
