import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred

pl_uri = 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret=cred.client_SECRET,
                                               redirect_uri=cred.redirect_url))

results = sp.playlist_tracks(pl_uri)["items"]
track_names = []
track_artists = []
artists_genres = []
tracks_popularities = []
tracks_release = []
i=1

for track in results:
    print(i)
    i += 1
    track_uri = track["track"]["uri"]

    #Track name
    track_name = track["track"]["name"]
    track_names.append(track_name)
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)

    #Name and genre
    artist_name = track["track"]["artists"][0]["name"]
    track_artists.append(artist_name)
    artist_genres = artist_info["genres"]
    artists_genres.append(artist_genres)
    
    #Popularity of the track
    track_pop = track["track"]["popularity"]
    tracks_popularities.append(track_pop)

    track_date = track["track"]['album']["release_date"]
    tracks_release.append(track_date)

print("Tracks names: %s" % (track_names))
print('\n')
print("Tracks artist: %s" % (track_artists))
print('\n')
print("Artists genre: %s" % (artists_genres))
print('\n')
print("Tracks popularity: %s" % (tracks_popularities))
print('\n')
print("Tracks release date: %s" % (tracks_release))