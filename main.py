import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred

nd_uri = 'spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret=cred.client_SECRET,
                                               redirect_uri=cred.redirect_url))

results = sp.artist_top_tracks(nd_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
