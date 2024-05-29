import os
import logging
import pandas as pd
from dotenv import load_dotenv

from utils import get_response

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch multiple tracks' details and audio features
def get_tracks_details_and_audio_features(track_ids, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    ids = ','.join(track_ids)
    
    # Fetch track details and audio features
    tracks_url = f"https://api.spotify.com/v1/tracks?ids={ids}"
    audio_features_url = f"https://api.spotify.com/v1/audio-features?ids={ids}"
    
    tracks_details = get_response(tracks_url, headers)['tracks']
    tracks_audio_features = get_response(audio_features_url, headers)['audio_features']

    return tracks_details, tracks_audio_features


id_df = pd.read_csv('track_ids_2.csv')
track_ids = id_df.track_id.values
res_df = pd.DataFrame(columns=['Track ID', 'Track Name', 'Artist Name', 'Danceability', 'Energy', 'Key',
                                'Loudness','Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness',
                                'Valence', 'Tempo', 'Duration (ms)'])
size = 2
for i in range(size, len(id_df), size):
    tracks_details, tracks_audio_features = get_tracks_details_and_audio_features(track_ids[i-size:i], access_token)

    for track, features in zip(tracks_details, tracks_audio_features):
        track_info = [track['id'],track['name'],track['artists'][0]['name'],features['danceability'],features['energy'],
                      features['key'], features['loudness'], features['mode'], features['speechiness'], features['acousticness'],
                      features['instrumentalness'], features['liveness'], features['valence'], features['tempo'], features['duration_ms']]

    res_df.loc[len(res_df)] = track_info
    res_df.to_csv('test.csv', index=False)
    logging.info(f"saved track {track['id']} ({track['name']}), i : {i}")
