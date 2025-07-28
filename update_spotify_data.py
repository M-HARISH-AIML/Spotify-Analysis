import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='ee38e61a33c84519ae0d1e79e1b3e6e8',
    client_secret='b2e5bd29f61a4dbf8caaac77937b00cd'
))

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'H@rish052005',
    'database': 'spotify_db'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

with open("track_urls.txt", 'r') as file:
    urls = file.readlines()

for url in urls:
    url = url.strip()
    try:
        track_id = re.search(r'track/([a-zA-Z0-9]+)', url).group(1)
        track = sp.track(track_id)

        data = {
            'Track Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration': track['duration_ms'] / 60000
        }

        insert_query = """
        INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data['Track Name'], data['Artist'], data['Album'], data['Popularity'], data['Duration']
        ))
        conn.commit()
    except Exception as e:
        print("Error:", e)

cursor.close()
conn.close()
