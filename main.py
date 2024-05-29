import os
import json
import logging
import pandas as pd
from dotenv import load_dotenv

from get_access import get_access_key

from utils import get_response

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Load environment variables
load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

def get_tracks_from_playlist(playlist_id, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    tracks = []
    cnt = 0
    while url:
        try:
            data = get_response(url, headers)
            tracks.extend(data['items'])
            url = data['next']
            cnt += 1
            logging.info(f"Processed page {cnt} of playlist {playlist_id}")
        except Exception as e:
            logging.error(f"Failed to get tracks from playlist {playlist_id}: {e}")
            break
    return tracks

def get_tracks_from_albums(album_id, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    tracks = []
    cnt = 0
    while url:
        try:
            data = get_response(url, headers)
            tracks.extend([track['id'] for track in data['items']])
            url = data['next']
            cnt += 1
            logging.info(f"Processed page {cnt} of album {album_id}")
        except Exception as e:
            logging.error(f"Failed to get tracks from album {album_id}: {e}")
            break
    return tracks


def get_featured_playlists(access_token, limit=50, offset=0):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/browse/featured-playlists?limit={limit}&offset={offset}"
    try:
        data = get_response(url, headers)
        playlists = data['playlists']['items']
        return [playlist['id'] for playlist in playlists]
    except Exception as e:
        logging.error(f"Failed to get featured playlists: {e}")
        return []

def get_category_playlists(category_id, access_token, limit=50, offset=0):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists?limit={limit}&offset={offset}"
    try:
        data = get_response(url, headers)
        playlists = data['playlists']['items']
        return [playlist['id'] for playlist in playlists]
    except Exception as e:
        logging.error(f"Failed to get playlists for category {category_id}: {e}")
        return []
        
    # Function to get albums
def get_albums(access_token, limit=50, offset=0, query=None, explore=False):
    headers = {"Authorization": f"Bearer {access_token}"}
    if explore:
        url = f"https://api.spotify.com/v1/browse/new-releases?limit={limit}&offset={offset}"
    else:
        url = f"https://api.spotify.com/v1/search?q={query}&type=album&limit={limit}&offset={offset}"
    try:
        data = get_response(url, headers)
        albums = data['albums']['items']
        return [album['id'] for album in albums]
    except Exception as e:
        logging.error(f"Failed to get playlists for {query} album: {e}")
        return []

def main():
    all_playlist_ids, all_album_ids = set(), set()

    for offset in range(0, 100, 50):
        featured_playlist_ids = get_featured_playlists(access_token, limit=50, offset=offset)
        all_playlist_ids.update(featured_playlist_ids)

    genres = get_response('https://api.spotify.com/v1/recommendations/available-genre-seeds', {"Authorization": f"Bearer {access_token}"})['genres']
    logging.info(f"Existing Genres: {genres[:10]} ...")
    
    for genre in genres:
        for offset in range(0, 200, 50):
            category_playlist_ids = get_category_playlists(genre, access_token, limit=50, offset=offset)
            all_playlist_ids.update(category_playlist_ids)

    logging.info(f"Collected {len(all_playlist_ids)} unique playlist IDs")
    
    with open('q.json', 'r') as f:
        queries = json.load(f)

    for ex in [True, False]:
        for query in queries if not ex else [None]:
            for offset in range(0, 100, 50):
                album_ids = get_albums(access_token, limit=50, offset=offset, query=query, explore=ex)
                all_album_ids.update(album_ids)    
        
    all_ids = []
    for playlist_id in all_playlist_ids:
        all_tracks = get_tracks_from_playlist(playlist_id, access_token)
        track_ids = [track['track']['id'] for track in all_tracks if track['track']]
        all_ids.extend(track_ids)

    for album_id in all_album_ids:
        all_tracks = get_tracks_from_albums(album_id, access_token)
        all_ids.extend(all_tracks)

    file_name = 'track_ids_2.csv'
    df = pd.DataFrame({'track_id': all_ids})
    df.to_csv(file_name, index=False)
    logging.info(f"Saved {len(df)} tracks to {file_name}")

if __name__ == "__main__":
    main()
