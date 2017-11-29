import PlaylistExtractor
import json
import pandas as pd

file_path = 'Data/pop.json'
with open(file_path , "r") as fd:
    playlists_raw = json.load(fd)
playlists_table = []

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

for pl_raw in playlists_raw:
    pl = {}
    print('extracting features for: {}'.format(pl_raw['name']))
    extractor = PlaylistExtractor.PlaylistExtractor(pl_raw)
    pl['followers'] = extractor.num_of_followers()
    pl['is_public'] = extractor.is_public()
    pl['no_of_songs'] = extractor.num_of_songs()
    pl['num_of_markets_avg'] = extractor.num_of_markets_avg()
    pl['song_popularity_avg'] = extractor.song_popularity_avg()
    pl['song_popularity_std'] = extractor.song_popularity_std()
    pl['song_duration_avg'] = extractor.song_duration_avg()
    pl['song_duration_std'] = extractor.song_duration_std()
    pl['num_of_artists'] = extractor.num_of_artists()
    for field in audio_fields:
        pl[field + '_avg'] = extractor.get_audio_feature_avg(field)
        pl[field + '_std'] = extractor.get_audio_feature_std(field)
    playlists_table.append(pl)

playlists_df = pd.DataFrame(playlists_table)
playlists_df.to_csv('data.csv')
