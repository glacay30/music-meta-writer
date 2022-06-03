# Music Meta Writer

Adds ffmpeg metadata to your music files based on csv data.

### Requires:
* Python 3.10
* ffmpeg

### How to Use:
`./music-meta-writer.py directory csv`
* `directory`: Directory where you have all of the song files. Accepted formats include mp3, mp4, and m4a.
* `csv`: The csv/tsv file to parse from. If you're data has commas, use tsv instead.

The format of the csv file should ideally look something like:

| metadata_key_0 | metadata_key_1 | etc
| --- | --- | ---
| example_0_0 | example_0_1
| example_1_0 | example_1_1
| etc

Where each metadata key aligns exactly with what ffmpeg expects (the full list of available metadata keys are [here](https://wiki.multimedia.cx/index.php/FFmpeg_Metadata)). For my application, I stuck to `album_artist, title, album, date`.
