import pickle
import os
import spotipy
import cred
from spotipy.oauth2 import SpotifyOAuth
from operator import attrgetter
from urllib.parse import _NetlocResultMixinBase
from distutils.log import error

path = 'data'
ORIGINAL_FILE = os.path.join(path, 'orig_file.bin')
PLAYLIST_FILE = os.path.join(path, 'playlist.bin')
ARTISTS_FILE = os.path.join(path, 'arts_file.bin')
ARTIST_POPULARITY_FILE = os.path.join(path, 'art_pop_file.bin')
GENRE_FILE = os.path.join(path, 'genre_file.bin')
TRACK_GENRE_FILE = os.path.join(path, 'trk_gen_file.bin')
POPULARITY_FILE = os.path.join(path, 'pop_file.bin')
DATE_FILE = os.path.join(path, 'date_file.bin')
OFFSET_FILE = os.path.join(path, 'offset.bin')
NAMES_FILE = os.path.join(path, 'names.bin')

pl_uri = 'spotify:playlist:674SUzRPvJhMtdbm1w4c3Q'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
    client_id=cred.client_ID, 
    client_secret=cred.client_SECRET,
    redirect_uri=cred.redirect_url
    )
)