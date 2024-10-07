import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from spotify_module import Tracks, Artists

def test_get_track_info():
    assert Tracks.get_track_info("7Hu8EwH6FLR3D2pGpRpVqf")["title"] == "Strawberry"

def test_get_artist_ids():
    assert Tracks.get_artist_ids("Aardwolf")[0] == "2jJiCTVyTBQt4lYaDslB8F"

def test_get_artist_albums():
    assert Tracks.get_artist_albums(["2jJiCTVyTBQt4lYaDslB8F"])[0]["name"] == "Nougat"