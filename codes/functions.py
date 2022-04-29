from includes.header import (pickle, os)
from structs.trees import (BTree, Trie)

def charToIndex(ch):
    return ord(ch)-ord(' ')

def input_loop(phrase, ch1, ch2):
    while True:
        order = input(phrase)
        if order != ch1 and order != ch2:
            print("Wrong. Type again.\n")
        else:
            break
    return order

def file_to_tree(unpickler):
    return unpickler.load()

def pickle_offset(offset, unpickler):
    for i in range(offset):
        unpickler.load()
    return unpickler.load()