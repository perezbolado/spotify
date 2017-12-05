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

    def active_period(self):
        return self.last_update - self.first_update()

    def number_of_artist_genres(self):
        tracks_artist = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        artist_genres = []
        for artist in tracks_artist:
            artist_genres = artist_genres + [performer['genres'] for performer in artist][0]
        return len(np.unique(artist_genres))

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

    def decade_ratio(self):
        track_albums = [tr['track']['album'] for tr in self.pl['tracks']['items']]
        decade_count = {};
        for i in range(1900, 2020, 10):
            decade_count[i] = 0

        for album in track_albums:
            precision = album['release_date_precision']
            if precision == 'year':
                decade = int(int(album['release_date'])/10)*10
            if precision == 'month':
                year = int(album['release_date'].split('-')[0])
                decade = int(year/10)*10
            if precision == 'day':
                decade = int(parse(album['release_date']).year/10)*10
            if decade >= 1900:
                decade_count[decade] += 1
            else:
                decade_count[1900] += 1

        for decade, frequency in decade_count.items():
            if frequency == 0:
                decade_count[decade] = 0
            else:
                decade_count[decade] = decade_count[decade]/len(track_albums)
        return decade_count

    def playlist_name_score(self):
        score = 0
        words = []
        word_freq = {}
        tracks_tags = [tr['track']['album'] for tr in self.pl['tracks']['items']]
        artists = [tr['track']['artists'] for tr in self.pl['tracks']['items']]
        for tags in tracks_tags:
            for tag in tags:
                words += tag.lower().split(' ')
        for name in [artist['name'] for artist in artists]:
            words += name.lower().relplace('[:.,]').split(' ')
        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        for word, count in word_freq:
            word_freq[word] = count/len(words)
        for word in np.unique(self.pl['name'].lower.split(' ')):
            if word in word_freq:
                score += word_freq[word]
        return score

    def get_playlists_tracks_audio_features(self):
        return [tr['track']['audio_features'] for tr in self.pl['tracks']['items']]

    def get_audio_feature_avg(self, feature):
        tracks_audio_features = self.get_playlists_tracks_audio_features()
        return np.mean([trf[feature] for trf in tracks_audio_features if trf is not None and trf[feature] is not None])

    def get_audio_feature_std(self, feature):
        tracks_audio_features = self.get_playlists_tracks_audio_features()
        return np.std([trf[feature] for trf in tracks_audio_features if trf is not None and trf[feature] is not None])
