def get_all_artist_songs(names):
    import requests
    import time
    import os
    from dotenv import load_dotenv
    load_dotenv()
    # Your client credentials
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")


    # Get access token
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    access_token = auth_response.json()['access_token']


    # Set up the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    # get artist IDs
    artist_names = names.split(", ")
    artist_ids = []
    for name in artist_names:
        search_url = f'https://api.spotify.com/v1/search?q={name}&type=artist'
        search_response = requests.get(search_url, headers=headers)
        artist_ids.append(search_response.json()['artists']['items'][0]['id']) 
        
    
    # Get artist's albums
    for id in artist_ids:
        albums_url = f'https://api.spotify.com/v1/artists/{id}/albums'
        albums_response = requests.get(albums_url, headers=headers)
        albums = albums_response.json()['items']
     
     
    # Get album's tracks

        all_tracks = []
        track_ids = []
        for album in albums:
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
            else:
                return
            track_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
            track_response = requests.get(track_url, headers=headers)
            if track_response.status_code == 200:
                track_resp2 = track_response.json()
                track_vals = track_resp2
                return [track_name, track_vals]
            else:
                print(f"Failed to fetch track {track_id}: Status code {track_response.status_code}")
                return None
        track_data=[]
        for track_id in track_ids:
            track_info = get_track_info(track_id)
            if track_info:
                track_data.append(track_info)
                
            time.sleep(0.01)
        all_tracks.extend(track_data)
    return all_tracks


if __name__ == "__main__":
    get_all_artist_songs()