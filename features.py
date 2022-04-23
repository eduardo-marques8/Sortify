from models import Playlist
from operator import attrgetter
from sort import sortArray

def sort_by_popularity(self):
    print("Classificando a playlist por ordem de popularidade.")
    sortArray(self.tracks, 'popularity')

def sort_by_most_language(self):
    print("WIP")

def sort_by_most_weekly_most_listened(self):
    print("WIP")

def sort_by_release_date(self):
    print("Classificando a playlist por ordem de data de lançamento.")
    sortArray(self.tracks, 'releaseDate')

def classify_by_artist(self):
    print("Classificando a playlist por artista (em ordem alfabética).")
    # Salva um array apenas com os artistas presentes na playlist
    getKeyArray = attrgetter('artist')
    _artists = list(map(getKeyArray, self.tracks))      
    artists = list(dict.fromkeys(_artists))     # Remove duplicados
    sortArray(artists)      # Utiliza a quicksort para ordenar em ordem alfabética
    classifiedTracks = []
    for artist in artists:
        i=0
        while i < len(self.tracks):
            if(self.tracks[i].artist.lower()==artist):
                classifiedTracks.append(self.tracks[i])
                # Cada vez que acha percorre o array, deixa a lista menor, aumentando eficiência
                self.tracks.pop(i)
                i-=1    # Como foi removido um elemento do array, decrementa o index de varredura
            i+=1
    # Substitui o array do objeto com o novo array classificado
    self.tracks = classifiedTracks

def setupPlaylistFeatures():
    Playlist.sort_by_popularity = sort_by_popularity
    Playlist.sort_by_most_language = sort_by_most_language
    Playlist.sort_by_most_weekly_most_listened = sort_by_most_weekly_most_listened
    Playlist.sort_by_release_date = sort_by_release_date
    Playlist.classify_by_artist = classify_by_artist