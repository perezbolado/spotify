import SpotifyDAO
import json

dao = SpotifyDAO.SpotifyDAO()

'''all playlists by category'''
category_ids = dao.get_list_of_categories()
for category in category_ids[7:]:
    playlists = dao.get_all_playlist_by_category(category)
    playlists = [dao.enrich_playlist(pl['owner']['id'], pl['id']) for pl in playlists]
    with open(category + '.json', 'w') as outfile:
        json.dump(playlists, outfile)

'''Search for all playlists with character a'''
playlists = dao.search('a', type='playlist', max_results=2050)
playlists = [dao.enrich_playlist(pl['owner']['id'], pl['id']) for pl in playlists]
with open('random_a.json', 'w') as outfile:
        json.dump(playlists, outfile)
