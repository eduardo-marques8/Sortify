# Searching a key on a B-tree in Python
import pickle

# Create a node
class BTreeNode:
  def __init__(self, leaf=False):
    self.leaf = leaf
    self.keys = []
    self.child = []


# Tree
class BTree:
  def __init__(self, t):
    self.root = BTreeNode(True)
    self.t = t

    # Insert node
  def insert(self, k):
    root = self.root
    if len(root.keys) == (2 * self.t):
      temp = BTreeNode()
      self.root = temp
      temp.child.insert(0, root)
      self.split_child(temp, 0)
      self.insert_non_full(temp, k)
    else:
      self.insert_non_full(root, k)

    # Insert nonfull
  def insert_non_full(self, x, k):
    i = len(x.keys) - 1
    if x.leaf:
      x.keys.append((None, None))
      while i >= 0 and k[0] < x.keys[i][0]:
        x.keys[i + 1] = x.keys[i]
        i -= 1
      x.keys[i + 1] = k
    else:
      while i >= 0 and k[0] < x.keys[i][0]:
        i -= 1
      i += 1
      if len(x.child[i].keys) == (2 * self.t):
        self.split_child(x, i)
        if k[0] > x.keys[i][0]:
          i += 1
      self.insert_non_full(x.child[i], k)

    # Split the child
  def split_child(self, x, i):
    t = self.t
    y = x.child[i]
    z = BTreeNode(y.leaf)
    x.child.insert(i + 1, z)
    x.keys.insert(i, y.keys[t - 1])
    z.keys = y.keys[t: (2 * t)]
    y.keys = y.keys[0: t - 1]
    if not y.leaf:
      z.child = y.child[t: 2 * t]
      y.child = y.child[0: t - 1]

  # Print the tree
  def print_tree(self, x, l=0):
    print("Level ", l, " ", len(x.keys), end=":")
    for i in x.keys:
      print(i, end=" ")
    print()
    l += 1
    if len(x.child) > 0:
      for i in x.child:
        self.print_tree(i, l)

  def rec_btree_to_file(self, x, pickler, reverse, l=0):
    for i in x.keys:
      pickler.dump(i)
    l += 1
    if len(x.child) > 0:
      for i in x.child:
        self.rec_btree_to_file(i, pickler, l)

  def btree_to_file(self, x, file, reverse=False):
    pickler = pickle.Pickler(file)
    if reverse:
      list.reverse(x.keys)
    self.rec_btree_to_file(x, pickler, reverse)
    file.close()

  def file_to_btree(self, filename):
    file = open(filename, 'rb')
    unpickler = pickle.Unpickler(file)
    while True:
      try:
        print(unpickler.load())
      except EOFError:
        break

  # Search key in the tree
  def search_key(self, k, x=None):
    if x is not None:
      i = 0
      while i < len(x.keys) and k > x.keys[i][0]:
        i += 1
      if i < len(x.keys) and k == x.keys[i][0]:
        return (x, i)
      elif x.leaf:
        return None
      else:
        return self.search_key(k, x.child[i])
      
    else:
      return self.search_key(k, self.root)

class TrieNode:
     
    # Trie node class
    def __init__(self):
        self.children = [None]*255
        self.value = []
        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False
 
class Trie:
     
    # Trie data structure class
    def __init__(self):
        self.root = self.getNode()
 
    def getNode(self):
     
        # Returns new trie node (initialized to NULLs)
        return TrieNode()
 
    def _charToIndex(self,ch):
         
        # private helper function
        # Converts key current character into index
        # use only 'a' through 'z' and lower case
         
        return ord(ch)-ord(' ')
 
 
    def insert(self,key,value):
         
        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
 
            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]
 
        # mark last node as leaf
        pCrawl.isEndOfWord = True
        pCrawl.value.append(value)
 
    def search(self, key):
         
        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]
 
        #return pCrawl.isEndOfWord
        return pCrawl.value

    def displayUtil(self,visited,node,str):
        index=0
        while index<255:
            if node.children[index]:
                str+=chr(32+index)
                if node.children[index].isEndOfWord == False:
                    self.displayUtil(visited,node.children[index],str)
                    str=str[0:(len(str)-1)]
                else:
                    if str not in visited:
                        visited.append((str, node.children[index].value))
                    if self.haschild(node.children[index]):
                        self.displayUtil(visited,node.children[index],str)
                        str=str[0:(len(str)-1)]
                     
            index+=1
     
    def haschild(self,node):
        for i in range(255):
            if node.children[i]:
                return True
        return False
    
    def display(self):
        visited=[]
        str=''
        self.displayUtil(visited,self.root,str)
        print("Content of Trie:")
        for i in range(len(visited)):
            print(visited[i])

    def trie_to_file(self, file, reverse=False):
        visited=[]
        str=''
        pickler = pickle.Pickler(file)
        self.displayUtil(visited,self.root,str)
        for i in range(len(visited)):
            pickler.dump(visited[i]) 
        file.close() 

def main():
  # Input keys (use only 'a' through 'z' and lower case)
    keys = ["the","a","there","anaswe","any",
            "by","their"]
    output = ["Not present in trie",
              "Present in trie"]
 
    # Trie object
    t = Trie()
 
    # Construct trie
    for key in keys:
        t.insert(key, 'test')
 
    # Search for different keys
    #print("{} ---- {}".format("the",output[t.search("the")]))
    #print("{} ---- {}".format("these",output[t.search("these")]))
    #print("{} ---- {}".format("their",output[t.search("their")]))
    #print("{} ---- {}".format("thaw",output[t.search("thaw")]))

    print(t.search('the'))
    t.display()


if __name__ == '__main__':
  main()