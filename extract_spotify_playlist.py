import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='ee38e61a33c84519ae0d1e79e1b3e6e8',
    client_secret='b2e5bd29f61a4dbf8caaac77937b00cd'
))

# Playlist ID from the URL
playlist_id = '7qnbdDEF5mJGWRJHGNCYgw'

# Fetch all tracks from playlist
track_urls = []
offset = 0
limit = 100

while True:
    response = sp.playlist_items(
        playlist_id,
        offset=offset,
        limit=limit,
        additional_types=['track']
    )

    items = response.get('items', [])
    if not items:
        break

    for item in items:
        track = item.get('track')
        if track and track.get('external_urls'):
            track_urls.append(track['external_urls']['spotify'])

    offset += len(items)
    if len(items) < limit:
        break

# Save to file
with open("track_urls.txt", "w") as file:
    for url in track_urls:
        file.write(url + "\n")

print(f"✅ Extracted {len(track_urls)} track URLs from the playlist.")
