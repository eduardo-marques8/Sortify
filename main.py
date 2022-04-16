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
    track_uri = track["track"]["uri"]

    #Track name
    track_name = track["track"]["name"]
    print("Name: %s" % (track_name))
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)

    #Name and genre
    artist_name = track["track"]["artists"][0]["name"]
    print("Artist: %s" % (artist_name))
    artist_genres = artist_info["genres"]
    print("Genre: %s" % (artist_genres))
    
    #Popularity of the track
    track_pop = track["track"]["popularity"]
    print("Popularity: %s" % (track_pop))

    track_date = track["track"]['album']["release_date"]
    print("Release date: %s" % (track_date))

    features = sp.audio_features(track_uri)[0]
    track_energy = features['energy']
    print("Track energy: %s" % (track_energy))

    print('\n')
    i += 1