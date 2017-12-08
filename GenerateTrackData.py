import json
import PlaylistExtractor

file_name = 'data/EveryNoise_playlists.txt'

with open(file_name, 'r') as f:
    with open(file_name+'_tracks.csv', 'a', encoding='utf-8') as track_file:
        print_tracks_header = True
        for line in f:
            plist = json.loads(line)
            extractor = PlaylistExtractor.PlaylistExtractor(plist)
            for track in plist['tracks']['items']:
                track_data = extractor.extract_track_features(track)
                if print_tracks_header:
                    track_file.write(','.join([str(v) for v in track_data.keys()]) + '\n')
                    print_tracks_header = False
                track_file.write(','.join([str(v) for v in track_data.values()]) + '\n')
