import SpotifyDAO
import json

dao = SpotifyDAO.SpotifyDAO()

#def playlist_to_csv( playlist )


#'''all playlists by category'''
#category_ids = dao.get_list_of_categories()
# for category in category_ids[7:]:
#    playlists = dao.get_all_playlist_by_category(category)
#    playlists = [dao.enrich_playlist(pl['owner']['id'], pl['id']) for pl in playlists]
#    with open(category + '.json', 'w') as outfile:
#        json.dump(playlists, outfile)

#'''Search for all playlists '''
#search = 'rock'
#playlists = dao.search(search, type='playlist', max_results=50)
#enriched_playlists = []
#for pl in playlists:
#    try:
#        enriched_playlists.append(dao.enrich_playlist(pl['owner']['id'], pl['id']))
#    except:
#        print('Unable to enrich {}'.format(pl))
#
#with open('random_{}.json'.format(search), 'w') as outfile:
#    json.dump(enriched_playlists, outfile)

user = 'spotify'
playlists = dao.get_user_playlists(user)
enriched_playlists = []
for pl in playlists:
    try:
        enriched_playlists.append(dao.enrich_playlist(pl['owner']['id'], pl['id']))
    except:
       print('Unable to enrich {}'.format(pl))

with open('user_{}.json'.format(user), 'w') as outfile:
    json.dump(enriched_playlists, outfile)