import csv
import os
import subprocess
import sys

from click import FileError


in_directory = sys.argv[1]
in_csv = sys.argv[2]

ACCEPTABLE_MUSIC_FORMATS = {"m4a", "mp3", "mp4"}

def is_title_on_disk(title: str, songs_on_disk):
    for song in songs_on_disk:
        filename, _ = song.rsplit(".", maxsplit=1)
        if title.lower() == filename.lower():
            return True, song
    return False, None

def is_acceptable_music_file(file: str):
    if not os.path.isfile(in_directory + file):
        return False

    _, extension = file.rsplit(".", maxsplit=1)

    for format in ACCEPTABLE_MUSIC_FORMATS:
        if extension == format:
            return True

    return False

songs_on_disk = {x for x in os.listdir(in_directory) if is_acceptable_music_file(x)}

with open(in_csv, newline='') as csv_file:

    csv_extension = in_csv.rsplit('.', maxsplit=1)[1]
    csv_delimiter = ""
    if csv_extension == "csv":
        csv_delimiter = ","
    elif csv_extension == "tsv":
        csv_delimiter = "\t"
    else:
        raise FileError(in_csv, "Cannot parse the given file if it isn't csv or tsv!")

    csv_file_reader = csv.DictReader(csv_file, delimiter=csv_delimiter)
    os.chdir(in_directory)

    for song in csv_file_reader:

        song_title = ""
        try:
            song_title = song["title"]
        except KeyError:
            continue

        on_disk, song_filename = is_title_on_disk(song_title, songs_on_disk)
        if not on_disk:
            continue

        commands = ["ffmpeg", "-i", song_filename]

        for k, v in song.items():
            if v is not None:
                commands.extend(["-metadata", f"{k}={v}"])

        temp_song_filename = "_" + song_filename
        commands.extend(["-c", "copy", "-y", temp_song_filename])

        subprocess.call(commands)

        os.replace(temp_song_filename, song_filename)
