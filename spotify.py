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


def get_all_artist_songs(names, dancey_val, dancey=False):
    # get artist IDs
    artist_names = names.split(", ")
    artist_ids = []
    for name in artist_names:
        search_url = f'https://api.spotify.com/v1/search?q={name}&type=artist'
        search_response = requests.get(search_url, headers=headers)
        artist_ids.append(search_response.json()['artists']['items'][0]['id']) 


    # Get artist's albums
    albums = []
    for id in artist_ids:
        albums_url = f'https://api.spotify.com/v1/artists/{id}/albums'
        albums_response = requests.get(albums_url, headers=headers)
        albums.extend(albums_response.json()['items'])
    
     
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
            track_info = get_track_info(track_id)
            if track_info:
                if dancey:                   
                    if track_info["danceability"] >= int(dancey_val)/100:
                        track_data.append(track_info)
                else:
                    track_data.append(track_info)
                     
                
            time.sleep(0.01)
    all_tracks.extend(track_data)
    return all_tracks




def get_track_info(track_id):
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
            else:
                print(f"Failed to fetch track {track_id}: Status code {track_response.status_code}")
                return None


def download_csv(data):
     output = StringIO()
     headers = ["title", "artist", "album", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "id", "uri", "track_href", "analysis_url", "duration_ms", "time_signature"]
     writer = csv.DictWriter(output, fieldnames = headers)
     writer.writeheader()
     pythonized = ast.literal_eval((data))
     for track in pythonized:
        writer.writerow(track)
     output.seek(0)
     return output.getvalue()


def get_artists(genre, popularity, popularity_val, limit):
    artists = []
    offset = 0
    hit_pop_val = False
    def request_artists():
        search_url = f'https://api.spotify.com/v1/search?q=genre%3A%22{genre}%22&type=artist&limit=10&offset={offset}'
        print(search_url)
        search_response = requests.get(search_url, headers=headers)
        print(search_response)
        for item in search_response.json()['artists']['items']:
            if item["popularity"] > int(popularity_val):
                artists.append({"name": item["name"], "popularity": item["popularity"]})
            else:
                    return True

    if popularity: 
         while not hit_pop_val:
            hit_pop_val = request_artists()
            offset+=10
    else:           
        while len(artists) < int(limit):
            hit_pop_val = request_artists()
            offset+=10
    
    return artists