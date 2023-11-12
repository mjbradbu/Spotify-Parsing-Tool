from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import lyricsgenius

class SpotifyAPI:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('client_id_spotify')
        self.client_secret = os.getenv('client_secret_spotify')
        self.token = None

    def get_token(self):
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

        url = 'https://accounts.spotify.com/api/token'
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        self.token = json_result['access_token']

    def get_auth_header(self):
        return {"Authorization": 'Bearer ' + self.token}

    def search_for_artist(self, artist_name):
        url = 'https://api.spotify.com/v1/search'
        headers = self.get_auth_header()
        query = f'q={artist_name}&type=artist&limit=1'

        query_url = url + "?" + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)['artists']['items']
        if len(json_result) == 0:
            print("This artist does not exist")
            return None
        else:
            return json_result[0]

    def get_songs(self, artist_id):
        url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=JP'
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)['tracks']
        return json_result

class GeniusAPI:
    def __init__(self, token):
        self.genius = lyricsgenius.Genius(token)
        self.genius.verbose = False
        self.genius.remove_section_headers = True

    def get_lyrics(self, song_name, artist_name):
        song = self.genius.search_song(song_name, artist_name)
        if song:
            return song.lyrics
        else:
            print("Lyrics not found.")
            return None

def set_artist_and_song():
    artist_name = input('Enter Artist: ')
    song_name = input('Enter Song: ')
    return artist_name, song_name

def get_top_songs(artist_name):
    load_dotenv()
    spotify = SpotifyAPI()
    spotify.get_token()
    artist = spotify.search_for_artist(artist_name)

    if artist:
        artist_id = artist['id']
        songs = spotify.get_songs(artist_id)
        songs = spotify.get_songs(artist_id)
        list_top_songs = [song['name'] for song in songs]
        return list_top_songs

if __name__ == "__main__":
    load_dotenv()
    spotify = SpotifyAPI()
    artist_name, song_name = set_artist_and_song()

    spotify.get_token()
    artist = spotify.search_for_artist(artist_name)


    if artist:
        artist_id = artist['id']
        songs = spotify.get_songs(artist_id)
        list_top_songs = [song['name'] for song in songs]
        genius_token = os.getenv('client_access_token_genius')
        genius_api = GeniusAPI(genius_token)
        genius_api.get_lyrics(song_name, artist_name)

