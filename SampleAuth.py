import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
offset_size = 50
once = True
playlist_total = 0;
count = 0
playlists_refs = [];
while True:
    playlists = sp.category_playlists(category_id='latin', limit=offset_size, offset=count)
    for playlist in playlists['playlists']['items']:
        playlists_refs.append({'id': playlist['id'], 'name': playlist['name']})
    count = count + offset_size + 1
    if count > playlists['playlists']['total']:
        break
print(playlists_refs)