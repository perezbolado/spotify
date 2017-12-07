import PlaylistExtractor
import json
import pandas as pd


def extract_features(pl_raw):
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
    print('extracting features for: {}'.format(pl_raw['name']))
    extractor = PlaylistExtractor.PlaylistExtractor(pl_raw)
    pl['followers'] = extractor.num_of_followers()
    pl['is_public'] = extractor.is_public()
    pl['is_collaborative'] = extractor.is_collaborative()
    pl['num_of_songs'] = extractor.num_of_songs()
    pl['num_of_markets_avg'] = extractor.num_of_markets_avg()
    pl['song_popularity_avg'] = extractor.song_popularity_avg()
    pl['song_popularity_std'] = extractor.song_popularity_std()
    pl['song_duration_avg'] = extractor.song_duration_avg()
    pl['song_duration_std'] = extractor.song_duration_std()
    pl['num_of_artists'] = extractor.num_of_artists()
    pl['artist_popularity_avg'] = extractor.artist_popularity_avg()
    pl['artist_popularity_std'] = extractor.artist_popularity_std()
    pl['artist_genres'] = extractor.number_of_artist_genres()
    pl['last_update'] = extractor.last_update()
    pl['first_update'] = extractor.first_update()
    pl['active_period'] = pl['last_update'] - pl['first_update']
    pl['playlist_name_length'] = extractor.playlist_name_length()
    pl['name_score'] = extractor.playlist_name_score()
    decade_ratio = extractor.decade_ratio()
    for decade, ratio in decade_ratio.items():
        pl['decade_{}'.format(decade)] = ratio

    for field in audio_fields:
        pl[field + '_avg'] = extractor.get_audio_feature_avg(field)
        pl[field + '_std'] = extractor.get_audio_feature_std(field)

    return pl

file_path = 'EveryNoise.json'
with open(file_path, "r") as fd:
    playlists_raw = json.load(fd)
playlists_table = []

for pl_raw in playlists_raw:
    try:
        pl = extract_features(pl_raw)
        playlists_table.append(pl)
    except:
        print('Unable to enrich {}'.format(pl_raw['name']))

playlists_df = pd.DataFrame(playlists_table)
playlists_df.to_csv('EveryNoise.csv')