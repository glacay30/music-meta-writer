import csv
import os
import subprocess

songs_present = {x.lower() for x in os.listdir() if "m4a" in x}

with open("beatles.csv", newline='') as file:
    file_reader = csv.reader(file, delimiter=',')
    next(file_reader) # skip header
    for row in file_reader:
        song_name, album, year = row
        song_file = f"{song_name}.m4a"

        if song_file.lower() not in songs_present:
            continue

        subprocess.call(["ffmpeg", "-i", song_file,
            "-metadata", "album_artist=The Beatles",
            "-metadata", f"title={song_name}",
            "-metadata", f"album={album}",
            "-metadata", f"date={year}",
            "-c", "copy",
            "-y", "_" + song_file])

        os.replace("_" + song_file, song_file)
