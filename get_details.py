import os
import requests
import pandas as pd

from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

# Function to fetch multiple tracks' details and audio features
def get_tracks_details_and_audio_features(track_ids, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    ids = ','.join(track_ids)
    
    # Fetch track details and audio features
    tracks_url = f"https://api.spotify.com/v1/tracks?ids={ids}"
    audio_features_url = f"https://api.spotify.com/v1/audio-features?ids={ids}"
    
    tracks_response = requests.get(tracks_url, headers=headers)
    audio_features_response = requests.get(audio_features_url, headers=headers)
    
    if tracks_response == 200 and audio_features_response == 200:
        tracks_details = tracks_response.json()['tracks']
        tracks_audio_features = audio_features_response.json()['audio_features']
    
        return tracks_details, tracks_audio_features
    elif tracks_response == 429 and audio_features_response == 429:
        ra1 = int(tracks_response.headers.get('Retry-After', 1))
        ra2 = int(tracks_response.headers.get('Retry-After', 1))
        
        return max(ra1, ra2)

# Example track IDs (add up to 50 track IDs here)
track_ids = ['7221xIgOnuakPdLqT0F3nP', '629DixmZGHc7ILtEntuiWE', '2qSkIjg1o9h3YT9RAgYN75', '4IadxL6BUymXlh8RCJJu7T', '2FQrifJ1N335Ljm3TjTVVf', '2OzhQlSqBEmt7hmkYxfT6m', '7fzHQizxTqy8wTXwlrgPQQ', '6tNQ70jh4OwmPGpYy6R2o9',
             '46kspZSY3aKmwQe7O77fCC', '1bjeWoagtHmUKputLVyDxQ', '6AI3ezQ4o3HUoP6Dhudph3', '2GxrNKugF82CnoRFbQfzPf', '17phhZDn6oGtzMe56NuWvj', '7BRD7x5pt8Lqa1eGYC4dzj', '0WbMK4wrZ1wFSty9F7FCgu', '4NJqhmkGN042BrvHoMKUrJ', '3qhlB30KknSejmIvZZLjOD', '4q5YezDOIPcoLr8R81x9qy', '5uQ7de4EWjb3rkcFxyEOpu', '51eSHglvG1RJXtL3qI5trr', '3rUGC1vUpkDG9CZFHMur1t', '0mflMxspEfB0VbI1kyLiAv', '0Z7nGFVCLfixWctgePsRk9']


# Fetch track details and audio features
tracks_details, tracks_audio_features = get_tracks_details_and_audio_features(track_ids, access_token)

# Prepare the data for the DataFrame
data = []
for track, features in zip(tracks_details, tracks_audio_features):
    track_info = {
        'Track Name': track['name'],
        'Artist Name': track['artists'][0]['name'],
        'Danceability': features['danceability'],
        'Energy': features['energy'],
        'Key': features['key'],
        'Loudness': features['loudness'],
        'Mode': features['mode'],
        'Speechiness': features['speechiness'],
        'Acousticness': features['acousticness'],
        'Instrumentalness': features['instrumentalness'],
        'Liveness': features['liveness'],
        'Valence': features['valence'],
        'Tempo': features['tempo'],
        'Duration (ms)': features['duration_ms']
    }
    data.append(track_info)

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
# df.to_csv('spotify_tracks.csv', index=False)

print(f"Saved {len(df)} tracks to 'spotify_tracks.csv'")

