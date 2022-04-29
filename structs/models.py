from includes.header import (pickle, error)
from codes.functions import (file_to_tree, pickle_offset)

class Track:
    def __init__(self, _name, _artist, _genre, _popularity, _releaseDate):
        self.name = _name
        self.artist = _artist
        self.genre = _genre
        self.popularity = _popularity
        self.releaseDate = _releaseDate

def print_track(play_file, offset, i):
    unpickler_play = pickle.Unpickler(play_file)
    track = pickle_offset(offset, unpickler_play)
    play_file.close()
    print(f"Track #{i} -> '{track.name}' from '{track.artist}'")
    try:
        print(f'     --> Genre: {track.genre}')
        print(f'     --> Popularity: {track.popularity}')
        print(f'     --> Release date: {track.releaseDate}')
    except error:
        print(error)


def printTracksDetail(file, sort):
    sort_file = open(sort, 'rb')
    unpickler_sort = pickle.Unpickler(sort_file)
    i=0
    
    while True:
        try:
            offset = file_to_tree(unpickler_sort)[1]
            if not isinstance(offset, list):
                play_file = open(file, 'rb')
                print_track(play_file, offset, i)
                i += 1
            else:
                for o in offset:
                    play_file = open(file, 'rb')
                    print_track(play_file, o, i)
                    i += 1
        except EOFError:
            break
    sort_file.close()
    play_file.close()