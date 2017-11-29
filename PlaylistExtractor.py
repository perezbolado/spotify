import numpy as np


class PlaylistExtractor:
    pl = None

    def __init__(self, playlist):
        # type: (object) -> object
        self.pl = playlist

    def num_of_followers(self):
        return self.pl['followers']['total']

    def is_public(self):
        return int(self.pl['public'])

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

    def num_of_artists(self):
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_ids =[];
        for artist in tracks_artist:
            artist_ids += [performer['id']for performer in artist]
        return len(np.unique(artist_ids))

    def get_playlists_tracks_audio_features(self):
        return [tr['track']['audio_features'] for tr in self.pl['tracks']['items']]

    def get_audio_feature_avg(self, feature):
        tracks_audio_features = self.get_playlists_tracks_audio_features()
        return np.mean([trf[feature] for trf in tracks_audio_features if trf is not None and trf[feature] is not None])

    def get_audio_feature_std(self, feature):
        tracks_audio_features = self.get_playlists_tracks_audio_features()
        return np.std([trf[feature] for trf in tracks_audio_features if trf is not None and trf[feature] is not None])
