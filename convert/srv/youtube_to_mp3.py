from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import help
from sql import init_db

import urllib.request
import sqlite3
import os
import sys
import json
from datetime import datetime
from csv import DictReader


def find_metadata_json(html, album_name):
    # adding 20 as there's 20 useless characters before we get to the opening bracket
    start_index = html.find('var ytInitialData')+20
    count = 1
    try:
        while True:
            count += 1
            char = html[start_index + count]
            if char == ';':
                end_index = start_index + count
                break

        data = json.loads(html[start_index:end_index])
        return data

    except Exception as e:
        help.log(f'Something went wrong finding metadata json for {album_name}. \nException: {e}')
        sys.exit(1)


def fetch_youtube_urls():
    # TODO: replace .csv with sqlite db
    with open('./albums.csv', 'r') as f:
        dict_reader = DictReader(f)
        albums = list(dict_reader)

    for album in albums:
        html = urllib.request.urlopen(album['url']).read()
        data = find_metadata_json(html, album['album_name'])

        # the number of songs in playlist
        total_songs = len(data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents'])
        
        for i in range(total_songs):
            song_title = data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents'][i]['playlistPanelVideoRenderer']['title']['simpleText']
            video_id = data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents'][i]['playlistPanelVideoRenderer']['videoId']
            final_url = f'https://youtube.com/watch?v={video_id}'

            con = sqlite3.connect('/srv/sql/music.db')
            cur = con.cursor()
            cur.execute("""INSERT INTO song VALUES (?, ?, ?)""", (album['album_name'], song_title, final_url))
            con.commit()

    return

# TODO: complete convert_mp3()
# def convert_mp3():
#     driver = help.init_chrome_driver()
#     mp3_convert_url = 'https://ytmp3.nu/'

if __name__ == '__main__':
    if os.path.exists('./sql/music.db'):
        pass
    else:
        init_db.create_db()
        help.log('Created music.db because it didn\'t exist.')

    help.log('Starting YouTube to mp3 conversion service...')

    try:
        fetch_youtube_urls()
        # convert_mp3()
    except Exception as e:
        help.log(f'Something went wrong during the conversion process! \nException: {e}')