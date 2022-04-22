from models import Playlist
from sort import sortArray

def sort_by_popularity(self):
    sortArray(self.tracks, 'popularity')

def sort_by_most_language():
    print("WIP")

def sort_by_most_weekly_most_listened():
    print("WIP")

def sort_by_release_date():
    print("WIP")

def setupPlaylistFeatures():
    Playlist.sort_by_popularity = sort_by_popularity
    Playlist.sort_by_most_language = sort_by_most_language
    Playlist.sort_by_most_weekly_most_listened = sort_by_most_weekly_most_listened
    Playlist.sort_by_release_date = sort_by_release_date