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
import time
import json
from datetime import datetime
from csv import DictReader
from ftfy import fix_text


def find_metadata_json(html, album_name):
    # adding 20 as there's 20 useless characters before we get to the opening bracket
    start_index = html.find('var ytInitialData')+20
    count = 1

    # try:
    while True:
        count += 1
        char = html[start_index + count]
        if char == ';':
            end_index = start_index + count
            break

    json_prep = html[start_index:end_index]

    data = json.loads(fix_text(json_prep))
    return data

    # except Exception as e:
    #     help.log(f'Something went wrong finding metadata json for {album_name}. \nException: {e}')
    #     sys.exit(1)


def fetch_youtube_urls():
    # TODO: replace .csv with sqlite db
    with open('/srv/albums.csv', 'r') as f:
        dict_reader = DictReader(f)
        albums = list(dict_reader)

    for album in albums:
        html = urllib.request.urlopen(album['url']).read().decode()
        data = find_metadata_json(html, album['album_name'])

        # the number of songs in playlist
        total_songs = len(data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents'])
        
        for i in range(total_songs):
            song_title = data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents'][i]['playlistPanelVideoRenderer']['title']['simpleText']
            video_id = data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents'][i]['playlistPanelVideoRenderer']['videoId']
            final_url = f'https://youtube.com/watch?v={video_id}'

            con = sqlite3.connect('./sql/music.db')
            cur = con.cursor()
            cur.execute("""INSERT INTO songs VALUES (?, ?, ?)""", (album['album_name'], song_title, final_url))
            con.commit()

    return

def finished(driver):
    user = input('Finished (y/n)?')
    if user != 'y' or user != 'n':
        print('(y/n) are the only acceptable answers. Try again.')
        finished(driver)
    else:
        if user == 'y':
            driver.quit()
            sys.exit(0)
        else:
            time.sleep(300)
            finished(driver)


# TODO: complete convert_mp3()
def convert_mp3():
    driver = help.init_chrome_driver()
    mp3_convert_url = 'https://ytmp3.nu/'

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

    for song in data:
        if song[0].lower() == 'night castle' or song[0].lower() == 'the christmas attic':
            driver.get(mp3_convert_url)

            # search = driver.find_element(By.XPATH, '/html/body/div[3]/form/input[1]')
            search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/input[1]')))
            search.send_keys(song[2])

            # convert = driver.find_element(By.XPATH, '/html/body/div[3]/form/input[3]')
            convert = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/input[3]')))
            convert.click()

            download = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/a[1]')))
            download.click()

    finished(driver)


if __name__ == '__main__':
    if os.path.exists('./sql/music.db'):
        pass
    else:
        init_db.create_db()
        help.log('Created music.db because it didn\'t exist.')

    help.log('Starting YouTube to mp3 conversion service...')

    try:
        # fetch_youtube_urls()
        convert_mp3()
    except Exception as e:
        help.log(f'Something went wrong during the conversion process! \nException: {e}')