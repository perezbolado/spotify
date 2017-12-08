import spotipy
import numpy as np
import musicbrainzngs

from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyDAO:
    MAX_QUERY_RESULTS = 50
    MB_UPC_CACHE = {}
    MB_ARTIST_CACHE = {}
    AUDIO_ANALYSIS_CACHE = {}

    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        musicbrainzngs.set_useragent('playlists-producer', '1.0', 'perezbolado@gmail.com')

    def get_all_playlist_by_category(self, category, query_results=50):
        """
            returns all the playlists for a category
        :param category:
        :param query_results:
        :return:
        """
        playlists_refs = []
        print('querying all playlists with category: {}', category)
        playlists = self.sp.category_playlists(category_id=category, limit=query_results)['playlists']
        while playlists:
            playlists_refs += playlists['items']
            if playlists['next']:
                playlists = self.sp.next(playlists)['playlists']
            else:
                playlists = None
        print('completed {} playlists for: {}'.format(len(playlists_refs), category))
        return playlists_refs

    def get_user_playlists(self, user):
        """
            return all the playlist for a spotify user
        :param user:
        :return:
        """
        playlists_refs = [];
        playlists = self.sp.user_playlists(user)
        while playlists:
            playlists_refs += playlists['items']
            if playlists['next']:
                playlists = self.sp.next(playlists)
            else:
                playlists = None
        print('completed {} playlists for: {}'.format(len(playlists_refs), user))
        return playlists_refs

    def enrich_playlist(self, user_id, playlist_id, get_audio_analysis=False, get_playlist_tags=False):
        """
            get an enriched playlist object
        :param user_id:
        :param playlist_id:
        :param get_audio_analysis:
        :param get_playlist_tags:
        :return:
        """
        tracks_refs = []
        playlist = self.sp.user_playlist(user_id, playlist_id)
        tracks = playlist['tracks']
        while tracks:
            tracks_refs = tracks_refs + [tr for tr in playlist['tracks']['items'] if tr['track']['id'] is not None]
            if tracks['next']:
                tracks = self.sp.next(tracks)
            else:
                tracks = None
        playlist['tracks']['items'] = tracks_refs
        audio_features = self.enrich_audio_features([tr['track']['id'] for tr in tracks_refs])
        for i in range(0, len(audio_features)):
            playlist['tracks']['items'][i]['track']['audio_features'] = audio_features[i]
            # gets track audio analysis from spotify api
            if get_audio_analysis:
                track_id = playlist['tracks']['items'][i]['track']['id']
                if track_id in self.AUDIO_ANALYSIS_CACHE:
                    playlist['tracks']['items'][i]['track']['audio_analysis'] = self.AUDIO_ANALYSIS_CACHE[track_id]
                else:
                    try:
                        audio_analysis = self.sp.audio_analysis(track_id)
                    except:
                        print("Unable to extract audio analysis from: {}".format(track_id))
                        audio_analysis = {}
                    self.AUDIO_ANALYSIS_CACHE[track_id] = audio_analysis
                playlist['tracks']['items'][i]['track']['audio_analysis'] = audio_analysis
        albums = self.get_albums_information([tr['track']['album']['id'] for tr in tracks_refs])
        for i in range(0, len(albums)):
            playlist['tracks']['items'][i]['track']['album'] = albums[i]
            # gets tags associated with the artist for each track from musicbrainz
            if get_playlist_tags:
                if 'upc' in albums[i]['external_ids']:
                    upc = albums[i]['external_ids']['upc']
                    try:
                        playlist['tracks']['items'][i]['track']['tags'] = self.get_tags_from_album_artist(upc)
                    except :
                        print("Something went wrong with the request: {}".format(upc))
                        playlist['tracks']['items'][i]['track']['tags'] =[]
                else:
                    playlist['tracks']['items'][i]['track']['tags'] = []
        tracks_artist = [tr['track']['artists'] for tr in playlist['tracks']['items']]
        artist_ids = []
        for artist in tracks_artist:
            artist_ids += [performer['id'] for performer in artist]
        artists_data = self.get_artist_information(artist_ids)
        for i in range(0, len(playlist['tracks']['items'])):
            for j in range(0, len(playlist['tracks']['items'][i]['track']['artists'])):
                if playlist['tracks']['items'][i]['track']['artists'][j] is not None:
                    artist_id = playlist['tracks']['items'][i]['track']['artists'][j]['id']
                    playlist['tracks']['items'][i]['track']['artists'][j] = artists_data[artist_id]
        print('enriched playlist:{}'.format(playlist['name']))
        return playlist

    def get_tags_from_album_artist(self, upc):
        """
            get artists tags fro album from music brainz
        :param upc: album upc
        :return:
        """
        album_tags = []
        if upc in self.MB_UPC_CACHE:
            return self.MB_UPC_CACHE[upc]

        response = musicbrainzngs.search_releases(query='barcode:{}'.format(upc))
        if response['release-count'] == 0:
            return []
        release = response['release-list'][0]
        for artist_credit in release['artist-credit']:
            if type(artist_credit) == str:
                continue
            artist_id = artist_credit['artist']['id']
            if artist_id in self.MB_ARTIST_CACHE:
                album_tags += self.MB_ARTIST_CACHE[artist_id]
            else:
                artist_info = musicbrainzngs.get_artist_by_id(artist_id, includes=['tags'])['artist']
                if'tag-list' in artist_info:
                    tags = [tag['name'] for tag in artist_info['tag-list']]
                    self.MB_ARTIST_CACHE[artist_id] = tags
                    album_tags += tags
        self.MB_UPC_CACHE[upc] = album_tags
        return album_tags

    def get_artist_information(self, artist_ids):
        """
            get artist information from spotify api
        :param artist_ids:
        :return:
        """
        results = {}
        artist_data = []
        artist_ids = np.unique(artist_ids)
        for i in range(0, len(artist_ids), self.MAX_QUERY_RESULTS):
            artist_data += self.sp.artists(artist_ids[i:i + self.MAX_QUERY_RESULTS])['artists']
        for i in range(0, len(artist_ids)):
            results[artist_ids[i]] = artist_data[i]
        return results

    def get_albums_information(self, album_ids, max_query=20):
        """
            get albums data from spotify
        :param album_ids:
        :param max_query:
        :return:
        """
        albums = []
        for i in range(0, len(album_ids), max_query):
            albums += self.sp.albums(album_ids[i:i + max_query])['albums']
        return albums

    def enrich_audio_features(self, track_ids):
        """
            get audio features for tracks
        :param track_ids:
        :return:
        """
        audio_features = []
        for i in range(0, len(track_ids), self.MAX_QUERY_RESULTS):
            audio_features += self.sp.audio_features(tracks=track_ids[i:i + self.MAX_QUERY_RESULTS])

        return audio_features

    def get_list_of_categories(self, country=None, locale=None):
        """
            get list of categories from spotify
        :param country:
        :param locale:
        :return:
        """
        cat_refs = [];
        categories = self.sp.categories(country, locale, limit=self.MAX_QUERY_RESULTS)['categories']
        while categories:
            cat_refs += categories['items']
            if categories['next']:
                categories = self.sp.next(categories)['categories']
            else:
                categories = None
        return [ref['id'] for ref in cat_refs]

    def search(self, q, query_type='playlist', market=None, max_results=None):
        """
            query the spotify search api
        :param q:
        :param query_type:
        :param market:
        :param max_results:
        :return:
        """
        res_refs = []
        type_map = {
            'playlist': 'playlists',
            'track': 'tracks',
            'album': 'albums',
            'artist': 'artists',
        }

        results = self.sp.search(q, self.MAX_QUERY_RESULTS, qurey_type=type, market=market)[type_map[query_type]]
        while results:
            res_refs += results['items']
            if max_results is not None and len(res_refs) + self.MAX_QUERY_RESULTS > max_results:
                break
            if results['next']:
                results = self.sp.next(results)[type_map[query_type]]
            else:
                results = None
        return res_refs
