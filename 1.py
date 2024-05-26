# Function to fetch multiple tracks' details
def get_tracks_details(track_ids, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    ids = ','.join(track_ids)
    url = f"https://api.spotify.com/v1/tracks?ids={ids}"
    response = requests.get(url, headers=headers)
    return response.json()['tracks']

# Function to fetch multiple tracks' audio features
def get_tracks_audio_features(track_ids, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    ids = ','.join(track_ids)
    url = f"https://api.spotify.com/v1/audio-features?ids={ids}"
    response = requests.get(url, headers=headers)
    return response.json()['audio_features']

# Example track IDs (add up to 50 track IDs here)
track_ids = ['7wLShogStyDeZvL0a6daN5', '6eI8B3QW20P68MCYMb4Etd', '7qoxdajngC0j9VXrcnephA']

# Fetch track details
tracks_details = get_tracks_details(track_ids, access_token)
for track in tracks_details:
    print(f"Track Name: {track['name']}, Artist Name: {track['artists'][0]['name']}")

# Fetch track audio features
tracks_audio_features = get_tracks_audio_features(track_ids, access_token)
for features in tracks_audio_features:
    print(f"Track ID: {features['id']}, Danceability: {features['danceability']}, Energy: {features['energy']}, Loudness: {features['loudness']}, Tempo: {features['tempo']}")
