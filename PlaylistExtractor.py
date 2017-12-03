import numpy as np
import datetime
from scipy import stats
from dateutil.parser import parse

class PlaylistExtractor:
    pl = None

    def __init__(self, playlist):
        # type: (object) -> object
        self.pl = playlist

    def num_of_followers(self):
        return self.pl['followers']['total']

    def is_public(self):
        return int(self.pl['public'])

    def is_collaborative(self):
        return int(self.pl['collaborative'])

    def num_of_songs(self):
        return len(self.pl['tracks']['items'])

    def num_of_markets_avg(self):
        return np.mean([len(tr['track']['available_markets']) for tr in self.pl['tracks']['items']])

    def song_popularity_avg(self):
        return np.mean([tr['track']['popularity'] for tr in self.pl['tracks']['items']])

    def song_popularity_std(self):
        return np.std([tr['track']['popularity'] for tr in self.pl['tracks']['items']])

    def song_duration_avg(self):
        return np.mean([tr['track']['duration_ms'] for tr in self.pl['tracks']['items']])

    def song_duration_std(self):
        return np.std([tr['track']['duration_ms'] for tr in self.pl['tracks']['items']])

    def playlist_name_length(self):
        return len(self.pl['name'])

    def artist_popularity_avg(self):
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_popularity = []
        for artist in tracks_artist:
            artist_popularity += [performer['popularity'] for performer in artist]
        return np.mean(artist_popularity)

    def artist_popularity_std(self):
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_popularity = []
        for artist in tracks_artist:
            artist_popularity += [performer['popularity'] for performer in artist]
        return np.std(artist_popularity)

    def last_update(self):
        add_times = [tr['added_at'] for tr in self.pl['tracks']['items']]
        add_times_dts = [parse(time).timestamp() for time in add_times if time is not None]
        return np.max(add_times_dts)

    def first_update(self):
        add_times = [tr['added_at'] for tr in self.pl['tracks']['items']]
        add_times_dts = [parse(time).timestamp() for time in add_times if time is not None]
        return np.min(add_times_dts)

    def number_of_artist_genres(self):
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_generes = []
        for artist in tracks_artist:
            artist_generes = artist_generes + [performer['genres'] for performer in artist][0]
        return len(np.unique(artist_generes))

    def top_artist_genre_ratio_in_playlist(self):
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_genres = []
        for artist in tracks_artist:
            artist_genres += [performer['genres'] for performer in artist][0]
        artist_genre_mode = stats.mode(artist_genres)
        ratio = artist_genres.count(artist_genre_mode)/len(artist_genres)
        return ratio

    def num_of_artists(self):
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_ids = []
        for artist in tracks_artist:
            artist_ids += [performer['id'] for performer in artist]
        return len(np.unique(artist_ids))

    def get_playlists_tracks_audio_features(self):
        return [tr['track']['audio_features'] for tr in self.pl['tracks']['items']]

    def get_audio_feature_avg(self, feature):
        tracks_audio_features = self.get_playlists_tracks_audio_features()
        return np.mean([trf[feature] for trf in tracks_audio_features if trf is not None and trf[feature] is not None])

    def get_audio_feature_std(self, feature):
        tracks_audio_features = self.get_playlists_tracks_audio_features()
        return np.std([trf[feature] for trf in tracks_audio_features if trf is not None and trf[feature] is not None])
