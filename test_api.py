import requests
import json

# Replace 'YOUR_API_KEY' with your actual Apple Music API key
api_key = 'YOUR_API_KEY'

# Replace 'Weezer' with the artist name you want to search for
artist_name = 'Weezer'

# Construct the URL for searching the artist on Apple Music API
search_url = f'https://api.music.apple.com/v1/catalog/us/search?term={artist_name}&limit=1'

# Set the headers with your API key
# headers = {
#     'Authorization': f'Bearer {api_key}',
# }

# Make the API request
response = requests.get(search_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Check if any results were found
    if 'results' in data and 'artists' in data['results']:
        artists = data['results']['artists']['data']
        if artists:
            # Get the artist ID for the first result
            artist_id = artists[0]['id']

            # Construct the URL to get the top songs of the artist
            top_songs_url = f'https://api.music.apple.com/v1/catalog/us/artists/{artist_id}/top-songs'

            # Make the API request for the top songs
            response = requests.get(top_songs_url, headers=headers)

            if response.status_code == 200:
                top_songs_data = response.json()
                if 'data' in top_songs_data and top_songs_data['data']:
                    # Print the JSON response for the most popular song
                    print(json.dumps(top_songs_data['data'][0], indent=2))
                else:
                    print("No top songs found for the artist.")
            else:
                print("Error fetching top songs:", response.status_code)
        else:
            print("Artist not found.")
    else:
        print("No results found.")
else:
    print("Error searching for the artist:", response.status_code)