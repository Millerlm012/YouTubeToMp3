import sqlite3

def create_db():
    connection = sqlite3.connect('/srv/sql/music.db')

    with open('/srv/sql/music_schema.sql') as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()

    print('Created music db successfully!')