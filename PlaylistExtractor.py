import numpy as np
import datetime
from scipy import stats
from dateutil.parser import parse

"""This class is initialized with an enriched playlists object and provides 
methods to generate predictors 
"""

class PlaylistExtractor:
    pl = None

    def __init__(self, playlist):
        # type: (object) -> object
        self.pl = playlist

    def num_of_followers(self):
        return self.pl['followers']['total']

    def is_public(self):
        """
            boolean value to check if playlist is collaborative
        :return:
        """
        return int(self.pl['public'])

    def is_collaborative(self):
        """
            boolean value to check if playlist is collaborative
        :return:
        """
        return int(self.pl['collaborative'])

    def num_of_songs(self):
        """
            returns the number of songs in the playlist
        :return:
        """
        return len(self.pl['tracks']['items'])

    def num_of_markets_avg(self):
        """
            returns the average number of markets where the tracks are available
        :return:
        """
        return np.mean([len(tr['track']['available_markets']) for tr in self.pl['tracks']['items']])

    def song_popularity_avg(self):
        """
            returns the average track popularity
        :return:
        """
        return np.mean([tr['track']['popularity'] for tr in self.pl['tracks']['items']])

    def song_popularity_std(self):
        """
            returns the standard deviation of the track popularity in playlist
        :return:
        """
        return np.std([tr['track']['popularity'] for tr in self.pl['tracks']['items']])

    def song_duration_avg(self):
        """
            return the average track duration
        :return:
        """
        return np.mean([tr['track']['duration_ms'] for tr in self.pl['tracks']['items']])

    def song_duration_std(self):
        """
            return the standard deviation of track duration
        :return:
        """
        return np.std([tr['track']['duration_ms'] for tr in self.pl['tracks']['items']])

    def playlist_name_length(self):
        """
            returns the playlist name lenght
        :return:
        """
        return len(self.pl['name'])

    def artist_popularity_avg(self):
        """
            returns the artist average popularity in the playlist
        :return:
        """
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_popularity = []
        for artist in tracks_artist:
            artist_popularity += [performer['popularity'] for performer in artist]
        return np.mean(artist_popularity)

    def artist_popularity_std(self):
        """
            returns the standard deviation of the track popularity in the playlist
        :return:
        """
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_popularity = []
        for artist in tracks_artist:
            artist_popularity += [performer['popularity'] for performer in artist]
        return np.std(artist_popularity)

    def last_update(self):
        """
            returns the time of insertion of the latest track in the playlist
        :return:
        """
        add_times = [tr['added_at'] for tr in self.pl['tracks']['items']]
        add_times_dts = [parse(time).timestamp() for time in add_times if time is not None]
        return np.max(add_times_dts)

    def first_update(self):
        """
            returns the time of insertion from the oldest track in the playlist
        :return:
        """
        add_times = [tr['added_at'] for tr in self.pl['tracks']['items']]
        add_times_dts = [parse(time).timestamp() for time in add_times if time is not None]
        return np.min(add_times_dts)

    def active_period(self):
        """
            returns the difference in seconds between the first and the last update in the playlist
        :return:
        """
        return self.last_update - self.first_update()

    def number_of_artist_genres(self):
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_genres = []
        for artist in tracks_artist:
            artist_genres = artist_genres + [performer['genres'] for performer in artist][0]
        return len(np.unique(artist_genres))

    def top_artist_genre_ratio_in_playlist(self):
        """
            returns the ratio of the playlist of the most popular genre in the playlist
        :return:
        """
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_genres = []
        for artist in tracks_artist:
            artist_genres += [performer['genres'] for performer in artist][0]
        artist_genre_mode = stats.mode(artist_genres)
        ratio = artist_genres.count(artist_genre_mode) / len(artist_genres)
        return ratio

    def num_of_artists(self):
        """
            returns the number of artists that participate in this playlist
        :return:
        """
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_ids = []
        for artist in tracks_artist:
            artist_ids += [performer['id'] for performer in artist]
        return len(np.unique(artist_ids))

    def decade_ratio(self):
        """
            returns a structure with playlist tracks decade ratio
        :return:
        """
        track_albums = [tr['track']['album'] for tr in self.pl['tracks']['items']]
        decade_count = {};
        for i in range(1900, 2020, 10):
            decade_count[i] = 0

        for album in track_albums:
            precision = album['release_date_precision']
            if precision == 'year':
                decade = int(int(album['release_date']) / 10) * 10
            if precision == 'month':
                year = int(album['release_date'].split('-')[0])
                decade = int(year / 10) * 10
            if precision == 'day':
                decade = int(parse(album['release_date']).year / 10) * 10
            if decade >= 1900:
                decade_count[decade] += 1
            else:
                decade_count[1900] += 1

        for decade, frequency in decade_count.items():
            if frequency == 0:
                decade_count[decade] = 0
            else:
                decade_count[decade] = decade_count[decade] / len(track_albums)
        return decade_count

    def playlist_name_score(self):
        """
            calculate a playlist name score based on the frequency of the tags associated with the artist
        :rtype: object
        """
        score = 0
        words = []
        word_freq = {}
        if 'tags' in self.pl['tracks']['items'][0]['track']:

            tracks_tags = [tr['track']['tags'] for tr in self.pl['tracks']['items']]
            artists = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
            for tags in tracks_tags:
                for tag in tags:
                    words += tag.lower().split(' ')
            for name in [artist[0]['name'] for artist in artists]:
                words += name.lower().split(' ')
            for word in words:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
            for word, count in word_freq.items():
                word_freq[word] = count / len(words)
                if word in self.pl['name']:
                    score += word_freq[word]
        return score

    def get_playlists_tracks_audio_features(self):
        """
            extract spotify audio feautres
        :return:
        """
        return [tr['track']['audio_features'] for tr in self.pl['tracks']['items']]

    def get_audio_feature_avg(self, feature):
        """
            calculates the average for a specific audio feature in the playlist
        :param feature: audio feature name
        :return:
        """
        tracks_audio_features = self.get_playlists_tracks_audio_features()
        return np.mean([trf[feature] for trf in tracks_audio_features if trf is not None and trf[feature] is not None])

    def get_audio_feature_std(self, feature):
        """
            calculates the standard deviation for a specific audio feature in the playlist
        :param feature:
        :return:
        """
        tracks_audio_features = self.get_playlists_tracks_audio_features()
        return np.std([trf[feature] for trf in tracks_audio_features if trf is not None and trf[feature] is not None])

    def extract_track_features(self, track):
        """
            extract track features
        :param track: track object
        :return:
        """
        track_data = {}
        genres = []
        for k, v in track['track']['audio_features'].items():
            track_data[k] = v
        for artist in track['track']['artists']:
            genres += artist['genres']
        track_data['genres'] = '|'.join(np.unique(genres))
        track_data['playlist_name'] = self.pl.replace('The Sound of ', '')
        track_data['artists'] = '|'.join([artist['name'] for artist in track['track']['artists']])
        track_data['popularity'] = track['track']['popularity']
        track_data['artist_popularity'] = np.mean(
            [artist['popularity'] for artist in track['track']['artists'] if artist['popularity'] is not None])
        track_data['explicit'] = track['track']['explicit']
        track_data['id'] = track['track']['id']
        return track_data

    def extract_features(self):
        """
            extract audio features the playlist
        :return: track features object
        """
        pl = {}
        audio_fields = [
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_ms",
            "time_signature"
        ]
        print('extracting features for: {}'.format(self.pl['name']))
        pl['followers'] = self.num_of_followers()
        pl['is_public'] = self.is_public()
        pl['is_collaborative'] = self.is_collaborative()
        pl['num_of_songs'] = self.num_of_songs()
        pl['num_of_markets_avg'] = self.num_of_markets_avg()
        pl['song_popularity_avg'] = self.song_popularity_avg()
        pl['song_popularity_std'] = self.song_popularity_std()
        pl['song_duration_avg'] = self.song_duration_avg()
        pl['song_duration_std'] = self.song_duration_std()
        pl['num_of_artists'] = self.num_of_artists()
        pl['artist_popularity_avg'] = self.artist_popularity_avg()
        pl['artist_popularity_std'] = self.artist_popularity_std()
        pl['artist_genres'] = self.number_of_artist_genres()
        pl['last_update'] = self.last_update()
        pl['first_update'] = self.first_update()
        pl['active_period'] = pl['last_update'] - pl['first_update']
        pl['playlist_name_length'] = self.playlist_name_length()
        pl['name_score'] = self.playlist_name_score()
        decade_ratio = self.decade_ratio()
        for decade, ratio in decade_ratio.items():
            pl['decade_{}'.format(decade)] = ratio

        for field in audio_fields:
            pl[field + '_avg'] = self.get_audio_feature_avg(field)
            pl[field + '_std'] = self.get_audio_feature_std(field)

        return pl
