import spotipy
import config
import json
import pandas as pd
import numpy as np
import pickle
from spotipy.oauth2 import SpotifyClientCredentials

from pprint import pprint

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID,
                                                           client_secret=config.SPOTIPY_CLIENT_SECRET))
                                                        

class getAudioFt():
    def __init__(self, pl_ID):
        self.pl_ID=pl_ID
    def getTable(self):
        tracks =[]
        tracklist = sp.playlist_items(self.pl_ID, fields='items.track.id, items.track.artists',  offset=0,)
        tracklist = tracklist['items']
        for x in range(len(tracklist)):
            if tracklist[x]['track'] == None:
                continue
            else:
                tracks.append(tracklist[x]['track']['id'])
 
        aft = sp.audio_features(tracks)
        aft_={}
        for x in range(len(aft)):
            if aft[x] == None:
                 continue
            else: 
                aft_[aft[x]['id']]=[aft[x]['danceability'],aft[x]['energy'],
                aft[x]['key'], aft[x]['loudness'],
                aft[x]['mode'],aft[x]['speechiness'],aft[x]['acousticness'],
                aft[x]['instrumentalness'],aft[x]['liveness'], aft[x]['valence'],
                aft[x]['tempo'],aft[x]['duration_ms'], aft[x]['time_signature']]
        df = pd.DataFrame.from_dict(aft_, orient='index', 
                                columns=['danceability','energy','key',
                                'loudness','mode','speechiness','acousticness','instrumentalness',
                                'liveness','valence','tempo','duration_ms','time_signature'])
        return df

class getSummary():
    def __init__(self, pl_ID):
        self.pl_ID=pl_ID
    def getTable_(self):
        df = getAudioFt(self.pl_ID).getTable()

        mean = df.mean(axis=0)
        mean = mean.to_list()

        std = df.std(axis=0)
        std = std.to_list()

        max = df.max(axis=0)
        max = max.to_list()

        min = df.min(axis=0)
        min = min.to_list()


        median = df.median(axis=0)
        median = median.to_list()
        stats = { "mean":mean, "std":std, "max":max, "min":min, "median":median}
    

        df = pd.DataFrame.from_dict(stats, orient='index', columns=['danceability','energy','key',
                                'loudness','mode','speechiness','acousticness','instrumentalness',
                                'liveness','valence','tempo','duration_ms','time_signature'])
        
        return df

class getSpecs():
    def __init__(self, pl_ID):
        self.pl_ID=pl_ID
    def getDict(self):
        tracks =[]
        tracklist = sp.playlist_items(self.pl_ID, fields='items.track.id, items.track.artists',  offset=0,)
        tracklist = tracklist['items']
        for x in range(len(tracklist)):
            if tracklist[x]['track'] == None:
                continue
            else:
                tracks.append(tracklist[x]['track']['id'])
        
        info = {}
        for y in tracks:
            pull = sp.track(y)
            coverArt = pull['album']['images'][1]['url']
            songName= pull['name']
            artists = pull['artists']

            artistIDs = []
            artistNames = []
            for z in artists:
                id = z['id']
                artistIDs.append(id)
                name = z['name']
                artistNames.append(name)

            pop = []
            genres = []
            for a in artistIDs:
                b = sp.artist(a)
                pop.append(b['popularity'])

                for c in b['genres']:
                    genres.append(c)
            
            info[y]={'name':songName,
                'coverArt':coverArt,
                'artist': artistNames,
                'artistIds':artistIDs,
                'artistPop':pop,
                'genres':genres
                }
        return info

class getA():
    def __init__(self, pl_ID):
        self.pl_ID=pl_ID
    def getTable(self):
        tracks =[]
        tracklist = sp.playlist_items(self.pl_ID, fields='items.track.id, items.track.artists',  offset=0,)
        tracklist = tracklist['items']
        for x in range(len(tracklist)):
            if tracklist[x]['track'] == None:
                continue
            else:
                tracks.append(tracklist[x]['track']['id'])
        l = sp.audio_features(tracks)
        return l

pl = getAudioFt("spotify:playlist:37i9dQZF1DX4JAvHpjipBk")
pl.getTable().to_csv('data/22-03-25/aftTable.csv')

pl_ = getSummary("spotify:playlist:37i9dQZF1DX4JAvHpjipBk")
pl_.getTable_().to_csv('data/22-03-25/summary.csv')

pl__ = getSpecs("spotify:playlist:37i9dQZF1DX4JAvHpjipBk")
dic = pl__.getDict()

with open('/Users/sabrinalem/Desktop/FriData_Functions/data/22-03-25/specs.json', 'w') as out:
    json.dump(dic, out)
# pl = getA("spotify:playlist:37i9dQZF1DX4JAvHpjipBk").getTable()
# # print(pl)
# print(len(pl))

