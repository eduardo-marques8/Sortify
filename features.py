from operator import attrgetter
from sort import sortArray
import pickle
from models import *
from trees import BTree, BTreeNode, Trie, TrieNode
import os

def sort_feature(file, order):
    open_file = open(file, 'rb')
    unpickler = pickle.Unpickler(open_file)
    array = []

    while True:
        try:
            pic = file_to_tree(unpickler)
            array.append(pic)
        except EOFError:
            break

    open_file.close()
    os.remove(file)
    sortArray(array, order)

    b_tree = BTree(len(array))

    for e in array:
        b_tree.insert((e[0], e[1]))
    
    b_tree.btree_to_file(b_tree.root, file = open(file, 'wb'), reverse=True if order == 'd' else False)
    print("Done.\n")

def _charToIndex(ch):
    return ord(ch)-ord(' ')

def search_feature(file, key):
    open_file = open(file, 'rb')
    unpickler = pickle.Unpickler(open_file)
    tree = Trie()

    while True:
        try:
            pic = file_to_tree(unpickler)
            for e in pic[1]:
                tree.insert(pic[0], e)
        except EOFError:
            break
        
    root = tree.root
    pCrawl = root
    length = len(key)
    for level in range(length):
        index = _charToIndex(key[level])
        if not pCrawl.children[index]:
            return False
        pCrawl = pCrawl.children[index]
 
    return pCrawl.value

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