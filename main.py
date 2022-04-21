import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from models import *

pl_uri = 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret=cred.client_SECRET,
                                               redirect_uri=cred.redirect_url))

results = sp.playlist_tracks(pl_uri)["items"]
playlist = Playlist([])
i=1

for track in results:
    track_uri = track["track"]["uri"]

    #Track name
    name = track["track"]["name"]
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)

    #Name and genre
    artist_name = track["track"]["artists"][0]["name"]

    artist_genres = artist_info["genres"]
    
    #Popularity of the track
    popularity = track["track"]["popularity"]

    #Release date
    date = track["track"]['album']["release_date"]

    track = Track(name, artist_name, popularity, date)
    playlist.addTrack(track)

playlist.printTracksDetail()
#playlist.printTracksOrder()