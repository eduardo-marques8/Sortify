from header import pickle

# Create a node
class BTreeNode:
  def __init__(self, leaf=False):
    self.leaf = leaf
    self.keys = []
    self.child = []


# B Tree
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

  # Delete a node
  def delete(self, x, k):
      t = self.t
      i = 0
      while i < len(x.keys) and k[0] > x.keys[i][0]:
          i += 1
      if x.leaf:
          if i < len(x.keys) and x.keys[i][0] == k[0]:
              x.keys.pop(i)
              return
          return

      if i < len(x.keys) and x.keys[i][0] == k[0]:
          return self.delete_internal_node(x, k, i)
      elif len(x.child[i].keys) >= t:
          self.delete(x.child[i], k)
      else:
          if i != 0 and i + 2 < len(x.child):
              if len(x.child[i - 1].keys) >= t:
                  self.delete_sibling(x, i, i - 1)
              elif len(x.child[i + 1].keys) >= t:
                  self.delete_sibling(x, i, i + 1)
              else:
                  self.delete_merge(x, i, i + 1)
          elif i == 0:
              if len(x.child[i + 1].keys) >= t:
                  self.delete_sibling(x, i, i + 1)
              else:
                  self.delete_merge(x, i, i + 1)
          elif i + 1 == len(x.child):
              if len(x.child[i - 1].keys) >= t:
                  self.delete_sibling(x, i, i - 1)
              else:
                  self.delete_merge(x, i, i - 1)
          self.delete(x.child[i], k)

  # Delete internal node
  def delete_internal_node(self, x, k, i):
      t = self.t
      if x.leaf:
          if x.keys[i][0] == k[0]:
              x.keys.pop(i)
              return
          return

      if len(x.child[i].keys) >= t:
          x.keys[i] = self.delete_predecessor(x.child[i])
          return
      elif len(x.child[i + 1].keys) >= t:
          x.keys[i] = self.delete_successor(x.child[i + 1])
          return
      else:
          self.delete_merge(x, i, i + 1)
          self.delete_internal_node(x.child[i], k, self.t - 1)

  # Delete the predecessor
  def delete_predecessor(self, x):
      if x.leaf:
          return x.pop()
      n = len(x.keys) - 1
      if len(x.child[n].keys) >= self.t:
          self.delete_sibling(x, n + 1, n)
      else:
          self.delete_merge(x, n, n + 1)
      self.delete_predecessor(x.child[n])

  # Delete the successor
  def delete_successor(self, x):
      if x.leaf:
          return x.keys.pop(0)
      if len(x.child[1].keys) >= self.t:
          self.delete_sibling(x, 0, 1)
      else:
          self.delete_merge(x, 0, 1)
      self.delete_successor(x.child[0])

  # Delete resolution
  def delete_merge(self, x, i, j):
      cnode = x.child[i]

      if j > i:
          rsnode = x.child[j]
          cnode.keys.append(x.keys[i])
          for k in range(len(rsnode.keys)):
              cnode.keys.append(rsnode.keys[k])
              if len(rsnode.child) > 0:
                  cnode.child.append(rsnode.child[k])
          if len(rsnode.child) > 0:
              cnode.child.append(rsnode.child.pop())
          new = cnode
          x.keys.pop(i)
          x.child.pop(j)
      else:
          lsnode = x.child[j]
          lsnode.keys.append(x.keys[j])
          for i in range(len(cnode.keys)):
              lsnode.keys.append(cnode.keys[i])
              if len(lsnode.child) > 0:
                  lsnode.child.append(cnode.child[i])
          if len(lsnode.child) > 0:
              lsnode.child.append(cnode.child.pop())
          new = lsnode
          x.keys.pop(j)
          x.child.pop(i)

      if x == self.root and len(x.keys) == 0:
          self.root = new

  # Delete the sibling
  def delete_sibling(self, x, i, j):
      cnode = x.child[i]
      if i < j:
          rsnode = x.child[j]
          cnode.keys.append(x.keys[i])
          x.keys[i] = rsnode.keys[0]
          if len(rsnode.child) > 0:
              cnode.child.append(rsnode.child[0])
              rsnode.child.pop(0)
          rsnode.keys.pop(0)
      else:
          lsnode = x.child[j]
          cnode.keys.insert(0, x.keys[i - 1])
          x.keys[i - 1] = lsnode.keys.pop()
          if len(lsnode.child) > 0:
              cnode.child.insert(0, lsnode.child.pop())

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

  def rec_btree_to_file(self, x, pickler, l=0):
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
    self.rec_btree_to_file(x, pickler)
    file.close()

  def print_tree(self, x, l=0):
    print("Level ", l, " ", len(x.keys), end=":")
    for i in x.keys:
      print(i, end=" ")
    print()
    l += 1
    if len(x.child) > 0:
      for i in x.child:
        self.print_tree(i, l)

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
 
    def _charToIndex(self, ch):
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
 
        return pCrawl.value

    def fileUtil(self,visited,node,str):
        index=0
        while index<255:
            if node.children[index]:
                str+=chr(32+index)
                if node.children[index].isEndOfWord == False:
                    self.fileUtil(visited,node.children[index],str)
                    str=str[0:(len(str)-1)]
                else:
                    if str not in visited:
                        visited.append((str, node.children[index].value))
                    if self.haschild(node.children[index]):
                        self.fileUtil(visited,node.children[index],str)
                        str=str[0:(len(str)-1)]
                     
            index+=1
     
    def haschild(self,node):
        for i in range(255):
            if node.children[i]:
                return True
        return False

    def trie_to_file(self, file):
        visited=[]
        str=''
        pickler = pickle.Pickler(file)
        self.fileUtil(visited,self.root,str)
        for i in range(len(visited)):
            pickler.dump(visited[i]) 
        file.close() 

    def display(self):
        visited=[]
        str=''
        self.fileUtil(visited,self.root,str)
        print("Content of Trie:")
        for i in range(len(visited)):
            print(visited[i])