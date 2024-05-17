import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from keys import lastfm_api_key, spotify_clientID, spotify_clientSecret
import numpy as np

class Song:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
        self.id = None
        self.details = None
        self.fv = None

    def get_song_details(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=spotify_clientID, client_secret=spotify_clientSecret)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        song_name = '+'.join(self.name.split())
        artist_name = '+'.join(self.artist.split())
        query = f'track={song_name}&artist={artist_name}'
        result = sp.search(q=query, limit=1)
        self.id = result['tracks']['items'][0]['id']
        self.details = dict(sp.audio_features(self.id)[0])
    
    def get_song_features(self):
        self.get_song_details()
        features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                     'liveness', 'valence', 'tempo', 'time_signature']
        feature_vector = np.zeros(len(features))

        for i in range(len(features)):
            feature_vector[i] = self.details[features[i]]
        
        self.fv = feature_vector


class User:
    def __init__(self, username):
        self.username = username #Last.fm username
        self.top_songs = None
    
    def fetch_top_songs(self, num=10):
        url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks'
        params = dict(
            user = self.username,
            api_key = lastfm_api_key,
            format = 'json',
            limit = num
        )
        r = requests.get(url=url, params=params)
        data = r.json()
        data = data['toptracks']['track']
        song_list = []
        for i in range(num):
            song_name = data[str(i)]['name']
            artist_name = data[str(i)]['artist']['name']
            song_list.append(Song(song_name,artist_name))
        self.top_songs = song_list



if __name__ == '__main__':
    song = Song('Good Luck', 'Broken Bells')
    song.get_song_features()