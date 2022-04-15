import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred

pl_uri = 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret=cred.client_SECRET,
                                               redirect_uri=cred.redirect_url))

results = sp.playlist_tracks(pl_uri)["items"]
i=1
for track in results:
    print(i)
    #Track name
    track_name = track["track"]["name"]
    print("Name: %s" % (track_name))
    
    #Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    print("Artist: %s" % (artist_name))
    
    #Popularity of the track
    track_pop = track["track"]["popularity"]
    print("Popularity: %s" % (track_pop))

    track_date = track["track"]['album']["release_date"]
    print("Release date: %s" % (track_date))

    track_duration = track['track']['duration_ms']
    print("Track duration: %s" % (track_duration))

    print('\n')
    i += 1