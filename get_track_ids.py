import os
import requests

access_token = 'BQB9bOxlCq-dQQ9dwkPqTqmHETBh5ZA7x6m7NO3IwKtldvnbtQZlrzc3EB5srV39YdgL01CU5dXMSoA3FatNcWI0YqRCrRtUsq95TLJ3-Gz-aXVqiUg'



# -------------- get with playlist -------------
# def get_tracks_from_playlist(playlist_id, access_token):
#     headers = {"Authorization": f"Bearer {access_token}"}
#     url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
#     tracks = []

#     while url:
#         response = requests.get(url, headers=headers)
#         data = response.json()
#         tracks.extend(data['items'])
#         url = data['next']  # URL for the next page of results

#     return tracks

# playlist_id = '4Jb4PDWREzNnbZcOHPcZPy'  
# # playlist_id = '37i9dQZF1DXcBWIGoYBM5M'  # Example playlist ID
# all_tracks = get_tracks_from_playlist(playlist_id, access_token)
# track_ids = [track['track']['id'] for track in all_tracks if track['track']]
# print(f"Collected {len(track_ids)} track IDs from playlist")
# print(track_ids)



# ----------- ---------------
# def get_featured_playlists(access_token, limit=50):
#     headers = {"Authorization": f"Bearer {access_token}"}
#     url = f"https://api.spotify.com/v1/browse/featured-playlists?limit={limit}"
#     response = requests.get(url, headers=headers)
#     print(response)
#     data = response.json()
#     playlists = data['playlists']['items']
#     return [playlist['id'] for playlist in playlists]

# featured_playlist_ids = get_featured_playlists(access_token)
# print(f"Collected {len(featured_playlist_ids)} featured playlist IDs")
# print(featured_playlist_ids)



# Function to get playlists with pagination
# def get_category_playlists(category_id, access_token, limit=50, offset=0):
#     headers = {"Authorization": f"Bearer {access_token}"}
#     url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists?limit={limit}&offset={offset}"
#     response = requests.get(url, headers=headers)
#     data = response.json()
#     playlists = data['playlists']['items']
#     return [playlist['id'] for playlist in playlists]

# # Example usage
# category_id = 'pop'
# all_playlist_ids = []

# # Fetch the first 200 playlists in increments of 50
# for offset in range(0, 200, 50):
#     playlist_ids = get_category_playlists(category_id, access_token, limit=50, offset=offset)
#     all_playlist_ids.extend(playlist_ids)

# print(f"Collected {len(all_playlist_ids)} playlist IDs from category '{category_id}'")




# Function to get featured playlists
def get_featured_playlists(access_token, limit=50, offset=0):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/browse/featured-playlists?limit={limit}&offset={offset}"
    response = requests.get(url, headers=headers)
    data = response.json()
    playlists = data['playlists']['items']
    return [playlist['id'] for playlist in playlists]

# Function to get playlists from a category with pagination
def get_category_playlists(category_id, access_token, limit=50, offset=0):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists?limit={limit}&offset={offset}"
    response = requests.get(url, headers=headers)
    data = response.json()
    playlists = data['playlists']['items']
    return [playlist['id'] for playlist in playlists]

# Combine featured and category playlists
all_playlist_ids = set()

# Get featured playlists (first 100 featured playlists in batches of 50)
for offset in range(0, 100, 50):
    featured_playlist_ids = get_featured_playlists(access_token, limit=50, offset=offset)
    all_playlist_ids.update(featured_playlist_ids)

# Get category playlists (example: pop, hiphop, chill)
categories = ['pop', 'hiphop', 'chill']
for category in categories:
    for offset in range(0, 200, 50):  # Adjust the range as needed
        category_playlist_ids = get_category_playlists(category, access_token, limit=50, offset=offset)
        all_playlist_ids.update(category_playlist_ids)

print(f"Collected {len(all_playlist_ids)} unique playlist IDs")
