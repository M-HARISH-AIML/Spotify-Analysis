import re
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import mysql.connector

# ✅ Spotify API Authorization using OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='7ae955693f224b679fc0abaad6996b13',
    client_secret='a4b9348c27754ccb92abe396752c15c4',
    redirect_uri='http://127.0.0.1:5000/callback',
    scope='user-library-read',
    cache_path='.cache'  # Save token locally
))

# ✅ MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'spotify_db'
}

# ✅ Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# ✅ Spotify Track URL
track_url = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"

# ✅ Extract track ID from URL
track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

# ✅ Fetch track and audio features
track = sp.track(track_id)
features = sp.audio_features([track_id])[0]

# ✅ Extract all metadata
track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000,
    'Danceability': features['danceability'],
    'Energy': features['energy'],
    'Valence': features['valence'],
    'Tempo': features['tempo'],
    'Explicit': track['explicit']
}

# ✅ Insert into MySQL
insert_query = """
INSERT IGNORE INTO spotify_tracks 
(track_name, artist, album, popularity, duration_minutes, danceability, energy, valence, tempo, explicit)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)'],
    track_data['Danceability'],
    track_data['Energy'],
    track_data['Valence'],
    track_data['Tempo'],
    track_data['Explicit']
))
connection.commit()

print(f"✅ Inserted: '{track_data['Track Name']}' by {track_data['Artist']}'")

# ✅ Close DB connection
cursor.close()
connection.close()
