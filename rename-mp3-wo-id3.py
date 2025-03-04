# import os
# import re

# def to_sentence_case(text):
#     """Convert a given string to sentence case."""
#     return text.capitalize() if text else text

# def rename_mp3_files(directory):
#     # Get a list of all MP3 files in the directory
#     mp3_files = [f for f in os.listdir(directory) if f.endswith(".mp3")]

#     for mp3_file in mp3_files:
#         file_path = os.path.join(directory, mp3_file)

#         # Search for the artist, feature keyword, feature artist, and title
#         match = re.search(r"^(.*?)\s*(f_|feat|ft)\s*(.*?)\s*-\s*(.*?)(\.mp3)?$", mp3_file, re.IGNORECASE)
#         if match:
#             artist = match.group(1).strip()  # Capture the artist
#             feature_keyword = match.group(2).strip()  # Capture the feature keyword (f_, feat, or ft)
#             feature_artist = match.group(3).strip()  # Capture the feature artist
#             title = match.group(4).strip()  # Capture the title

#             # Remove any numbers preceded by a dash and any special characters following them
#             title = re.sub(r'-\s*\d+[\.\-]*', '', title)

#             # Convert the title to sentence case
#             title = to_sentence_case(title)

#             # Format the new filename
#             new_filename = f"{artist} - {title} {feature_keyword} {feature_artist}.mp3"
#             new_file_path = os.path.join(directory, new_filename)

#             # Rename the file
#             os.rename(file_path, new_file_path)
#             print(f"Renamed '{mp3_file}' to '{new_filename}'")
#         else:
#             # If no match, keep the file as it is
#             print(f"No match in '{mp3_file}'")

# if __name__ == "__main__":
#     target_directory = "/Users/muneer78/Downloads/rename"
#     rename_mp3_files(target_directory)

import os
import re

def to_title_case(text):
    """Convert a given string to title case (capitalize each word)."""
    return ' '.join(word.capitalize() for word in text.split())

def rename_mp3_files(directory):
    # Get a list of all MP3 files in the directory
    mp3_files = [f for f in os.listdir(directory) if f.lower().endswith(".mp3")]

    for mp3_file in mp3_files:
        file_path = os.path.join(directory, mp3_file)

        # Search for the artist and title in the filename
        match = re.search(r"^(.*?)\s*-\s*(.*?)(\.mp3)?$", mp3_file, re.IGNORECASE)
        if match:
            artist = match.group(1).strip()  # Capture the artist
            title = match.group(2).strip()  # Capture the title

            # Remove any numbers preceded by a dash and any special characters following them
            title = re.sub(r'[-\s]*\d+[\.\-]*', '', title)  # Removes numbers and special characters after them
            title = re.sub(r'\s+', ' ', title).strip()  # Remove extra spaces

            # Convert the title to title case
            title = to_title_case(title)

            # Format the new filename
            new_filename = f"{artist} - {title}.mp3"
            new_file_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed '{mp3_file}' to '{new_filename}'")
        else:
            # If no match, keep the file as it is
            print(f"No match in '{mp3_file}'")

if __name__ == "__main__":
    target_directory = "/Users/muneer78/Downloads/videos"
    rename_mp3_files(target_directory)
