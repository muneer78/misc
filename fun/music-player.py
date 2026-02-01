import os
import random
import subprocess

music_folder = "focus_music"
songs = [os.path.join(music_folder, f) for f in os.listdir(music_folder)]
subprocess.run(["open", random.choice(songs)])