import PlaylistExtractor
import json
import pandas as pd
import numpy as np


def extract_track_features(track,pl_name):
    track_data = {}
    genres = []
    for k,v in track['track']['audio_features'].items():
        track_data[k]=v
    for artist in track['track']['artists']:
        genres += artist['genres']
    track_data['genres'] = ' '.join(np.unique(genres))
    track_data['playlist_name'] = pl_name.replace('Sounds Of ')
    track_data['artists'] = ' '.join([artist['name'] for artist in track['track']['artists']])
    track_data['id'] = track['track']['id']
    return track_data

file_path = 'EveryNoise.json'
with open(file_path, "r") as fd:
    playlists_raw = json.load(fd)

tracks_table = []

for pl_raw in playlists_raw:
    for track in pl_raw['tracks']['items']:
        try:
            tr = extract_track_features(track, pl_raw['name'])
            print('extracted: {}'.format(track['track']['name']))
            tracks_table.append(tr)
        except:
            print('unable to extract track data'.format(track))

tracks_df = pd.DataFrame(tracks_table)
tracks_df.to_csv('EveryNoise.tracks.csv')

