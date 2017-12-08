import SpotifyDAO
import requests
import json
import csv
import numpy as np
import PlaylistExtractor
from bs4 import BeautifulSoup

def extract_track_features(track, pl_name):
    track_data = {}
    genres = []
    for k, v in track['track']['audio_features'].items():
        track_data[k] = v
    for artist in track['track']['artists']:
        genres += artist['genres']
    track_data['genres'] = '|'.join(np.unique(genres))
    track_data['playlist_name'] = pl_name.replace('The Sound of ', '')
    track_data['artists'] = '|'.join([artist['name'] for artist in track['track']['artists']])
    track_data['popularity'] = track['track']['popularity']
    track_data['artist_popularity'] = np.mean([artist['popularity'] for artist in track['track']['artists'] if artist['popularity'] is not None])
    track_data['explicit'] = track['track']['explicit']
    track_data['id'] = track['track']['id']
    return track_data

dao = SpotifyDAO.SpotifyDAO()
url = 'http://everynoise.com/everynoise1d.cgi?scope=all'
r = requests.get(url);
soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find("table")
rows = table.find_all("tr")
playlists = []
pl_data = [];
for row in rows:
    cols = row.find_all('td')
    if len(cols) == 3:
        entry = {
            'id': cols[1].contents[1].attrs['href'].split('=')[1].split(':')[4],
            'user': cols[1].contents[1].attrs['href'].split('=')[1].split(':')[2],
            'genre': cols[2].text.strip(),
        }
        playlists.append(entry)

print_data_header = True
for pl in playlists:
    try:
        print_tracks_header = True
        print('procesing: {}'.format(pl['id']))
        plist = dao.enrich_playlist(pl['user'], pl['id'])
        extractor = PlaylistExtractor.PlaylistExtractor(plist)
        plist_extracted_features = extractor.extract_features()
        with open('data/EveryNoise_playlists.txt', 'a') as outfile:
            outfile.write(json.dumps(plist) + '\n')
        with open('data/EveryNoise_playlists_data.csv', 'a') as data_outfile:
            if print_data_header:
                data_outfile.write(','.join([str(v) for v in plist_extracted_features.keys()]) + '\n')
                print_data_header = False
            data_outfile.write(','.join([str(v) for v in plist_extracted_features.values()]) + '\n')
        print_tracks_header = True
        with open('data/EveryNoise_tracks.csv', 'a') as track_file:
            for track in plist['tracks']['items']:
                track_data = extract_track_features(track, plist['name'])
                if print_tracks_header:
                    track_file.write(','.join([str(v) for v in track_data.keys()]) + '\n')
                    print_tracks_header = False
                track_file.write(','.join([str(v) for v in track_data.values()]) + '\n')
    except:
        print('unable to get playlist: id:{} genre:{}'.format(pl['id'], pl['genre']))
