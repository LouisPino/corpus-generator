import requests
import time

# Your client credentials


# Get access token
auth_url = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(auth_url, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})
access_token = auth_response.json()['access_token']

# Set up the headers
headers = {
    'Authorization': f'Bearer {access_token}',
}

# Artist ID
artist_ids = ['2YZyLoL8N0Wb9xBt1NhZWg', '5j93hwFBNo29RJMsWvtzj8']

# Get artist's albums
for idx, id in enumerate(artist_ids):
    albums_url = f'https://api.spotify.com/v1/artists/{artist_ids[idx]}/albums'
    albums_response = requests.get(albums_url, headers=headers)
    albums = albums_response.json()['items']

    track_ids = []
    for album in albums:
        # Get album's tracks
        tracks_url = album['href'] + '/tracks'
        tracks_response = requests.get(tracks_url, headers=headers)
        tracks = tracks_response.json()['items']
        
        for track in tracks:
            track_ids.append(track['id'])

    def get_track_info(track_id):
        track_url = f'https://api.spotify.com/v1/tracks/{track_id}'
        track_response = requests.get(track_url, headers=headers)
        if track_response.status_code == 200:
            track_resp = track_response.json()
            track_name = track_resp['name']
        track_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
        track_response = requests.get(track_url, headers=headers)
        if track_response.status_code == 200:
            track_resp2 = track_response.json()
            track_vals = track_resp2
            return [track_name, track_vals]
        else:
            print(f"Failed to fetch track {track_id}: Status code {track_response.status_code}")
            return None

    for track_id in track_ids:
        track_info = get_track_info(track_id)
        if track_info:
            print(track_info)
            print()
        time.sleep(0.01)  