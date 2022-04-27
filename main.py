from cmath import phase
from operator import attrgetter
from matplotlib import artist
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from models import *
import pickle
from trees import *
from features import *
import os

path = 'data'
ORIGINAL_FILE = os.path.join(path, 'orig_file.bin')
PLAYLIST_FILE = os.path.join(path, 'playlist.bin')
ARTISTS_FILE = os.path.join(path, 'arts_file.bin')
ARTIST_POPULARITY_FILE = os.path.join(path, 'art_pop_file.bin')
GENRE_FILE = os.path.join(path, 'genre_file.bin')
TRACK_GENRE_FILE = os.path.join(path, 'trk_gen_file.bin')
POPULARITY_FILE = os.path.join(path, 'pop_file.bin')
DATE_FILE = os.path.join(path, 'date_file.bin')

pl_uri = 'spotify:playlist:674SUzRPvJhMtdbm1w4c3Q'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
    client_id=cred.client_ID, 
    client_secret=cred.client_SECRET,
    redirect_uri=cred.redirect_url
    )
)

def input_loop(phrase, ch1, ch2):
    while True:
        order = input(phrase)
        if order != ch1 and order != ch2:
            print("Wrong. Type again.\n")
        else:
            break
    return order

def fetch_data(orig_tree, arts_tree, genre_tree, pop_tree, date_tree):
    results = sp.playlist_tracks(pl_uri)["items"]
    playlist_file = open(PLAYLIST_FILE, 'wb')
    pickler = pickle.Pickler(playlist_file)
    offset = 0

    for track in results:
        track_uri = track["track"]["uri"]

        #Track name
        name = track["track"]["name"]
        
        #Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)

        #Name and genre
        artist_name = track["track"]["artists"][0]["name"]

        try:
            artist_genre = artist_info["genres"][0]
        except IndexError:
            artist_genre = "not specified"
        
        #Popularity of the track
        popularity = track["track"]["popularity"]

        #Release date
        date = track["track"]['album']["release_date"]

        track = Track(name, artist_name, artist_genre, popularity, date)
        orig_tree.insert((offset, offset))
        arts_tree.insert(artist_name, (popularity, offset))
        genre_tree.insert(artist_genre, offset)
        pop_tree.insert((popularity, offset))
        date_tree.insert((date, offset))
        offset += 1
        pickler.dump(track)
        
    orig_tree.btree_to_file(orig_tree.root, file = open(ORIGINAL_FILE, 'wb'))
    arts_tree.trie_to_file(file = open(ARTISTS_FILE, 'wb'))
    genre_tree.trie_to_file(file = open(GENRE_FILE, 'wb'))
    pop_tree.btree_to_file(pop_tree.root, file = open(POPULARITY_FILE, 'wb'))
    date_tree.btree_to_file(date_tree.root, file = open(DATE_FILE, 'wb'))
    playlist_file.close()
    return offset
'''
def fetch_more_data(orig_tree, pop_tree, fetch_offset):
    results = sp.playlist_tracks(pl_uri, offset=fetch_offset)["items"]
    playlist_file = open(PLAYLIST_FILE, 'wb')
    pickler = pickle.Pickler(playlist_file)

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
        orig_tree.insert((fetch_offset, fetch_offset))
        pop_tree.insert((popularity, fetch_offset))
        fetch_offset += 1
        pickler.dump(track)
        
    orig_tree.btree_to_file(orig_tree.root, file = open(ORIGINAL_FILE, 'wb'))
    pop_tree.btree_to_file(pop_tree.root, file = open(POPULARITY_FILE, 'wb'))
    playlist_file.close()
    return fetch_offset
'''
def main():
    fetch_offset = 0

    try:
        playlist_file = open(PLAYLIST_FILE, 'rb')
        orig_file = open(ORIGINAL_FILE, 'rb')
        arts_file = open(ARTISTS_FILE, 'rb')
        genre_file = open(GENRE_FILE, 'rb')
        pop_file = open(POPULARITY_FILE, 'rb')
        date_file = open(DATE_FILE, 'rb')
        playlist_file.close()
        orig_file.close()
        arts_file.close()
        genre_file.close()
        pop_file.close()
        date_file.close()
    except FileNotFoundError:
        os.mkdir(path)
        orig_tree = BTree(10)
        arts_tree = Trie()
        genre_tree = Trie()
        pop_tree = BTree(10)
        date_tree = BTree(10)
        print("Fetching API data ...")
        fetch_offset = fetch_data(orig_tree, arts_tree, genre_tree, pop_tree, date_tree)
        print("Done!\n")

    print("Welcome to Sortify!")
    last_sort = ORIGINAL_FILE

    while True:
        print("What do you want to do?")
        print("\t - 1 - Print data on screen (by last sort - default is order of fetched data);")
        print("\t - 2 - Search tracks of given artist and classify by most listened;")
        print("\t - 3 - Search or classify tracks by genre;")
        print("\t - 4 - Classify playlist by week's most listened;")
        print("\t - 5 - Classify playlist's tracks by release date;")
        #print("\t - 6 - Add more data;")
        #print("\t - 7 - Remove data;")
        #print("\t - 8 - Update data;")
        print("\t - any - Quit.")
        op = input("Choose an option: ")

        if op == '1':
            printTracksDetail(PLAYLIST_FILE, last_sort)
        elif op == '2':
            key = input("Who are you searching for? ")
            value = search_feature(ARTISTS_FILE, key)
            if not value:
                print("The artist was not found in the playlist.\n")
            else:
                b_tree = BTree(len(value))
                for e in value:
                    b_tree.insert((e[0], e[1]))
                b_tree.btree_to_file(b_tree.root, file = open(ARTIST_POPULARITY_FILE, 'wb'))
                order = input_loop("Descending or ascending [d/a]? ", 'd', 'a')
                print("\nClassifying by popularity...")
                sort_feature(ARTIST_POPULARITY_FILE, order)
                last_sort = ARTIST_POPULARITY_FILE
        elif op == '3':
            choice = input_loop("Search or sort? " , 'search', 'sort')
            if choice == 'search':
                key = input("What genre are you looking for? ")
                value = search_feature(GENRE_FILE, key)
                if not value:
                    print("This genre was not found in the playlist.\n")
                    choice = ''
                else:
                    b_tree = BTree(len(value))
                    for e in value:
                        b_tree.insert((key, e))
                    b_tree.btree_to_file(b_tree.root, file = open(TRACK_GENRE_FILE, 'wb'))
                    printTracksDetail(PLAYLIST_FILE, TRACK_GENRE_FILE)
                    last_sort = TRACK_GENRE_FILE
            elif choice == 'sort':
                order = input_loop("Descending or ascending [d/a]? ", 'd', 'a')
                print("\nClassifying by genre...")
                sort_feature(GENRE_FILE, order)
                last_sort = GENRE_FILE
        elif op == '4':
            order = input_loop("Descending or ascending [d/a]? ", 'd', 'a')
            print("\nClassifying by popularity...")
            sort_feature(POPULARITY_FILE, order)
            last_sort = POPULARITY_FILE
        elif op == '5':
            order = input_loop("Descending or ascending [d/a]? ", 'd', 'a')
            print("\nClassifying by release date...")
            sort_feature(DATE_FILE, order)
            last_sort = DATE_FILE
        elif op == '6':
            print(fetch_offset)
            orig_tree = BTree(10)
            pop_tree = BTree(10)
            print("\nFetching more data ...")
            #fetch_offset = fetch_more_data(orig_tree, pop_tree, fetch_offset)
            print("Done.\n")
            last_sort = ORIGINAL_FILE
        else:
            print('out')
            break

if __name__ == '__main__':
  main()