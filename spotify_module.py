import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()
from io import StringIO 
import csv 
import json 
import ast



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

class Tracks:
    def get_all_artist_songs(data):
        # get artist IDs
        artist_ids = Tracks.get_artist_ids(data["artist_names"])
        albums = Tracks.get_artist_albums(artist_ids)
        del data["artist_names"]
        for track in Tracks.get_album_tracks(albums, data):
             yield track
    
    def get_artist_ids(names):
        artist_names = names.split(", ")
        artist_ids = []
        for name in artist_names:
            search_url = f'https://api.spotify.com/v1/search?q={name}&type=artist'
            search_response = requests.get(search_url, headers=headers)
            # return search_response.json()['artists']['items'][0]['id']
            artist_ids.append(search_response.json()['artists']['items'][0]['id']) 
        return artist_ids
        
    def get_artist_albums(artist_ids):
        # Get artist's albums
        albums = []
        for id in artist_ids:
            albums_url = f'https://api.spotify.com/v1/artists/{id}/albums'
            albums_response = requests.get(albums_url, headers=headers)
            albums.extend(albums_response.json()['items'])
        return albums
        
    def get_album_tracks(albums, filters):    
        # Get album's tracks
        all_tracks = []
        track_ids = []
        for album in albums:
                tracks_url = album['href'] + '/tracks'
                tracks_response = requests.get(tracks_url, headers=headers)
                tracks = tracks_response.json()['items']
                for track in tracks:
                    track_ids.append(track['id'])
        
        track_data=[]
        for track_id in track_ids:
                track_info = Tracks.get_track_info(track_id)
                if track_info == 429:
                    yield 429
                    return
                valid = True
                if track_info: 
                        for k in filters.keys():
                            if k == "tempo" or k == "loudness":
                                 if track_info[k] < int(filters[k]):
                                    valid = False
                                    break
                            elif track_info[k] < int(filters[k])/100:
                                 valid = False
                                 break
                                            
                        if valid:
                            track_data.append(track_info)
                            yield track_info
                time.sleep(0.01)
        all_tracks.extend(track_data)
        return (all_tracks, 200)

    def get_track_info(track_id):
        # get track data
            track_url = f'https://api.spotify.com/v1/tracks/{track_id}'
            track_response = requests.get(track_url, headers=headers)
            if track_response.status_code == 200:
                track_resp = track_response.json()
                track_name = track_resp['name']
                track_album = track_resp["album"]["name"]
                track_artist = track_resp["artists"][0]["name"]
            else:
                return
            track_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
            track_response = requests.get(track_url, headers=headers)
            if track_response.status_code == 200:
                track_resp2 = track_response.json()
                track_vals = track_resp2
                track_vals["title"] = track_name
                track_vals["album"] = track_album
                track_vals["artist"] = track_artist
                del track_vals["type"]
                return track_vals
            elif track_response.status_code == 429:
                 return 429
            else:
                print(f"Failed to fetch track {track_id}: Status code {track_response.status_code}.")
                return None

class Csv:
    def download(data):
        output = StringIO()
        headers = ["title", "artist", "album", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "id", "uri", "track_href", "analysis_url", "duration_ms", "time_signature"]
        writer = csv.DictWriter(output, fieldnames = headers)
        writer.writeheader()
        pythonized = ast.literal_eval((data))
        for track in pythonized:
            writer.writerow(track)
        output.seek(0)
        return output.getvalue()

class Artists: 
    def get(genre, popularity_val, limit):
        artists = []
        offset = 0
        def request_artists():
            search_url = f'https://api.spotify.com/v1/search?q=genre%3A%22{genre}%22&type=artist&limit=10&offset={offset}'
            search_response = requests.get(search_url, headers=headers)
            if search_response.status_code == 200:
                for item in search_response.json()['artists']['items']:
                        if item["popularity"] >= int(popularity_val) and len(artists) < int(limit):
                            yield {"name": item["name"], "popularity": item["popularity"]}
                            artists.append({"name": item["name"], "popularity": item["popularity"]})
                        else:
                            return True
            else:
                print(f"Error, Code {search_response.status_code}")

        while isinstance(limit, str) and len(artists) < int(limit) and offset <= 1000:
                for artist in request_artists():
                     yield artist
                offset+=10