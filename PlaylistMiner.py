import SpotifyDAO
import json

dao = SpotifyDAO.SpotifyDAO()
category = 'latin'
playlists = dao.get_all_playlist_by_category(category)
playlists = [dao.enrich_playlist(pl['owner']['id'], pl['id']) for pl in playlists]
with open(category + '.json', 'w') as outfile:
    json.dump(playlists, outfile)
