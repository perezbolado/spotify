import SpotifyDAO
import json

dao = SpotifyDAO.SpotifyDAO()

'''all playlists by category'''
#category_ids = dao.get_list_of_categories()
#for category in category_ids[7:]:
#enriched_playlists = []
#category  = 'blues'
#playlists = dao.get_all_playlist_by_category('blues')
#for pl in playlists:
#    try:
#        enriched_playlists.append(dao.enrich_playlist(pl['owner']['id'], pl['id']))
#    except:
#        print('Unable to enrich {}'.format(pl))
#with open(category + '.json', 'w') as outfile:
#    json.dump(enriched_playlists, outfile)

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


#user = 'spotify'
#playlists = dao.get_user_playlists(user)
#enriched_playlists = []
#for pl in playlists:
#    try:
#        enriched_playlists.append(dao.enrich_playlist(pl['owner']['id'], pl['id']))
#    except:
#       print('Unable to enrich {}'.format(pl))

#with open('user_{}4.json'.format(user), 'w') as outfile:
#    json.dump(enriched_playlists, outfile)

#dao.enrich_playlist('spotify', '37i9dQZF1DX0XUsuxWHRQd')