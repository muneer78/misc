import os
import re
import glob
from mutagen.easyid3 import EasyID3

path = '/Users/muneer78/Downloads/rename'
files = glob.glob(os.path.join(path, "*.mp3"))

for fname in files:
    try:
        track = EasyID3(fname)
        track_num = track.get('tracknumber', ['00'])[0].split('/')[0]  # Default to '00' if missing
        track_title = track.get('title', ['Unknown Title'])[0]
        track_title = re.sub(r'/', '_', track_title)

        # Pad single-digit track numbers
        track_num = track_num.zfill(2)

        # Construct new filename
        new_fname = os.path.join(path, f"{track_num} {track_title}.mp3")

        # Rename file if different from current name
        if fname != new_fname:
            os.rename(fname, new_fname)
            print(f"Renamed: '{fname}' -> '{new_fname}'")
    except Exception as e:
        print(f"Error processing '{fname}': {e}")
