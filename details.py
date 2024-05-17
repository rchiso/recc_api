import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from keys import lastfm_api_key, spotify_clientID, spotify_clientSecret
import numpy as np
from recc import find_similar_songs

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
    
    def fetch_top_songs(self, num=20):
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
            song_name = data[i]['name']
            artist_name = data[i]['artist']['name']
            song = Song(song_name, artist_name)
            song.get_song_features()
            song_list.append(song)
        self.top_songs = song_list
        return self.top_songs


if __name__ == '__main__':
    #song = Song('Good Luck', 'Broken Bells')
    #song.get_song_features()
    username1 = 'qfu10'
    username2 = 'Thundera77'
    user1 = User(username1)
    user2 = User(username2)
    ts1 = user1.fetch_top_songs(num=50)
    ts2 = user2.fetch_top_songs(num=50)
    reccs = find_similar_songs(ts1, ts2, num=5)
    for recc in reccs:
        print(f'Song Name = {recc.name}, Artist = {recc.artist}')

