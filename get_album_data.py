import spotipy
import config #config holds client secret and client id to access Spotify 
import pandas as pd

# use spotipy Spotify-API wrapper
from spotipy.oauth2 import SpotifyClientCredentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID,
                                                           client_secret=config.SPOTIPY_CLIENT_SECRET))

#########album audio features##############
class getAlbum_Aft:
    def __init__(self, album_ID):
        self.album_ID=album_ID
    def getTable(self):
        tracks =[]
        tracklist = sp.album_tracks(self.album_ID, limit=50)  #Spotify GET for specific album tracklist
        tracklist = tracklist['items']
        for x in range(len(tracklist)):
            tracks.append(tracklist[x]['id'])                 #Add only track id's to list       
        l = sp.audio_features(tracks)

        aft = sp.audio_features(tracks)                       #Spotify GET for audio features from tracklist
        aft_table={}
        for x in range(len(aft)):
            if aft[x] == None:
                 continue
            else:                                             #Create data frame for each track and it's audio features
                aft_table[aft[x]['id']]=[aft[x]['danceability'],aft[x]['energy'],
                aft[x]['key'], aft[x]['loudness'],
                aft[x]['mode'],aft[x]['speechiness'],aft[x]['acousticness'],
                aft[x]['instrumentalness'],aft[x]['liveness'], aft[x]['valence'],
                aft[x]['tempo'],aft[x]['duration_ms'], aft[x]['time_signature']]
        df = pd.DataFrame.from_dict(aft_table, orient='index', 
                                columns=['danceability','energy','key',
                                'loudness','mode','speechiness','acousticness','instrumentalness',
                                'liveness','valence','tempo','duration_ms','time_signature'])
        return df


##########summarize audio features for an album############
class getAlbum_Aft_Summary: 
    def __init__(self, album_ID):
        self.album_ID=album_ID
    def getTable(self):
        df = getAlbum_Aft(self.album_ID).getTable()     #call audio features dataframe for specific album id

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

        df = pd.DataFrame.from_dict(stats, orient='index', columns=['danceability','energy','key',   # create pandas dataframe of summary
                                'loudness','mode','speechiness','acousticness','instrumentalness',
                                'liveness','valence','tempo','duration_ms','time_signature'])
        
        return df



class getAlbum_Specs:
    def __init__(self, album_ID, year, win):
        self.album_ID=album_ID
        self.year=year
        self.win = win
    def getTable(self):
        tracklist = sp.album_tracks(self.album_ID, limit=50)      #Spotify GET for specific album tracklist
        tracklist = tracklist['items']
        album = sp.album(self.album_ID,)

        specs = []
        album_name = album['name']                              #Sort through Spotify GET for specific album specs
        album_id = self.album_ID
        artist_name = tracklist[0]['artists'][0]['name']
        artist_id = tracklist[0]['artists'][0]['id']
        year = self.year
        number_tracks = album["total_tracks"]
        win = self.win 

        aft = getAlbum_Aft_Summary(self.album_ID)              #add audio features summary to album specs 
        aft = aft.getTable().iloc[0].tolist()

        

        specs.extend([album_name,album_id,artist_name,artist_id, year, number_tracks, win])
        specs.extend(aft)

        df = pd.DataFrame(specs).T                            #create pandas data frame of album's specs
        df.columns = ['album_name','album_id', 'artist_name', 'artist_id','year', 'number_tracks', 'win', 'danceability','energy','key','loudness',"mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","duration_ms","time_signature"]
        return df

   

#######################CONVERTING TO CSV and Master Data Doc#######################################
    
#Below are functions that create csv files for each dataframe for each album 
# Each specs dataframe is appended to a master csv file which will be used for data analysis

##############ALBUM 1 CSV CREATION##################################
# audioft = getAlbum_Aft("albumID").getTable()
# audioft= audioft.to_csv('data/year/albumx/aft.csv')

# summary = getAlbum_Aft_Summary("albumID").getTable()
# summary = summary.to_csv('data/year/albumx/summary.csv')

# specs = getAlbum_Specs("albumID", year, win(numeric 0 or 1)).getTable()
# specs_ = specs.to_csv('data/year/albumx/specs.csv')



