from includes.header import (PLAYLIST_FILE, pickle, os)
from structs.trees import (BTree, Trie)
from codes.sort import sortArray
from codes.functions import (charToIndex, file_to_tree)

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
    
    b_tree.btree_to_file(b_tree.root, file = open(file, 'ab'), reverse=True if order == 'd' else False)
    print("Done.\n")

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
        index = charToIndex(key[level])
        if not pCrawl.children[index]:
            return False
        pCrawl = pCrawl.children[index]
 
    return pCrawl.value