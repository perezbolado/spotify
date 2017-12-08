import SpotifyDAO
import json
import PlaylistExtractor
dao = SpotifyDAO.SpotifyDAO()

'''all playlists by category'''
#category_ids = dao.get_list_of_categories()
#for category in category_ids[7:]:
#enriched_playlists = []
#category  = 'blues'
#playlists = dao.get_all_playlist_by_category('blues')
#for pl in playlists:


'''get playlist using the search engine '''
#search = 'rock'
#playlists = dao.search(search, type='playlist', max_results=50)
#enriched_playlists = []
#for pl in playlists:

'''get playlists by user'''
#user = 'spotify'
#playlists = dao.get_user_playlists(user)
#enriched_playlists = []

file_prefix = 'data/playlists'
for pl in playlists:
    try:
        print_tracks_header = True
        print('procesing: {}'.format(pl['id']))
        plist = dao.enrich_playlist(pl['user'], pl['id'])
        extractor = PlaylistExtractor.PlaylistExtractor(plist)
        plist_extracted_features = extractor.extract_features()
        with open(file_prefix + '_raw.txt', 'a') as outfile:
            outfile.write(json.dumps(plist) + '\n')
        with open(file_prefix+'_data.csv', 'a') as data_outfile:
            if print_data_header:
                data_outfile.write(','.join([str(v) for v in plist_extracted_features.keys()]) + '\n')
                print_data_header = False
            data_outfile.write(','.join([str(v) for v in plist_extracted_features.values()]) + '\n')
        print_tracks_header = True
        with open(file_prefix+'_tracks.csv', 'a') as track_file:
            for track in plist['tracks']['items']:
                track_data = extractor.extract_track_features(track)
                if print_tracks_header:
                    track_file.write(','.join([str(v) for v in track_data.keys()]) + '\n')
                    print_tracks_header = False
                track_file.write(','.join([str(v) for v in track_data.values()]) + '\n')
    except:
        print('unable to get playlist: id:{} genre:{}'.format(pl['id'], pl['genre']))