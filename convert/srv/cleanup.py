import os
import sqlite3

con = sqlite3.connect('./sql/music.db')
cur = con.cursor()
data = cur.execute("""SELECT * FROM songs""").fetchall()
"""
data outline:
- 3 columns
- data[0] = album_name
- data[1] = song_name
- data[2] = url
"""
song_names = []
album_names = []
for row in data:
    song_names.append(row[1])
    album_names.append(row[0])


files = os.listdir('./data')
for file in files:
    if '.mp3' in file:
        song_name = file[:-4]
        if song_name in song_names:
            index = song_names.index(song_name)
            album_name = album_names[index].lower()
            os.rename(f'./data/{song_name}.mp3', f'./data/{album_name}/{song_name}.mp3')