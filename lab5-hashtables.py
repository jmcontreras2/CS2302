#CS2302 Fall 2019 MW 10:30 A.M. - 11:50 A.M
#Author: Jonatan M. Contreras
#Assignment: Lab 5 - NLP Implementation - Hash Tables
#Instructor: Dr. Olac Fuentes
#TA: PhD Student Anindita Nath
#Peer Leader: Diego Rodriguez
#Date of Last Modification: 11/03/2019

#Purpose of Program: The purpose of this program is to store a large amount of words
#and their embeddings in four different data structures: BSTrees, BTrees, Hash Tables 
#with Chaining and Hash Tables with Linear Probing. Further, the program allows the user
#to compute similarities between desired pairs of words using these various data structures.

import numpy as np
import time

###################### BST CLASS AND FUNCTIONS ################################
class BST(object):
    def __init__(self, data, left=None, right=None):  
        self.data = data
        self.left = left 
        self.right = right      
    
#InsertBST was modified to work with WordEmbedding objects.
def InsertBST(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.data.word > newItem.word:
        T.left = InsertBST(T.left,newItem)
    else:
        T.right = InsertBST(T.right,newItem)
    return T

#SearchBST was modified to work with WordEmbedding objects.
def searchBST(T, k):
    if k == T.data.word:
        return T
    elif k > T.data.word:
        a = searchBST(T.right, k)
        return a
    else:
        b = searchBST(T.left, k)
        return b
    
def numberOfNodes(T):
    if T is not None:
        return 1 + numberOfNodes(T.left) + numberOfNodes(T.right)
    else:
        return 0
    
def heightBST(T):
    if T is None:
        return 0
    left = heightBST(T.left)
    right = heightBST(T.right)
    return 1 + max(left, right)

############################B-TREE CLASS AND FUNCTIONS#########################

class BTree(object):
    # Constructor
    def __init__(self,data,child=[],isLeaf=True,max_data=5):  
        self.data = data
        self.child = child 
        self.isLeaf = isLeaf
        if max_data <3: #max_data must be odd and greater or equal to 3
            max_data = 3
        if max_data%2 == 0: #max_data must be odd and greater or equal to 3
            max_data +=1
        self.max_data = max_data
#FindChild was modified to work with WordEmbedding objects.
def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree   
    for i in range(len(T.data)):
        if k.word < T.data[i].word:
            return i
    return len(T.data)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.data.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_data//2
    if T.isLeaf:
        leftChild = BTree(T.data[:mid],max_data=T.max_data) 
        rightChild = BTree(T.data[mid+1:],max_data=T.max_data) 
    else:
        leftChild = BTree(T.data[:mid],T.child[:mid+1],T.isLeaf,max_data=T.max_data) 
        rightChild = BTree(T.data[mid+1:],T.child[mid+1:],T.isLeaf,max_data=T.max_data) 
    return T.data[mid], leftChild,  rightChild   

#InsertLeaf was modified to work with WordEmbedding objects.
def InsertLeaf(T,i):
    T.data.append(i)  
    T.data.sort(key = lambda WordEmbedding: WordEmbedding.word)

def IsFull(T):
    return len(T.data) >= T.max_data

def InFullNode(T, k):
    t = SearchBtree(T, k)
    if t == None:
        return False
    a = IsFull(t)
    return a
 
def InsertBtree(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.data =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)      
     
def HeightBtree(T):
    if T.isLeaf:
        return 0
    return 1 + HeightBtree(T.child[0])    
 
#SearchBtree was modified to work with WordEmbedding objects.
def SearchBtree(T,k):
    # Returns node where k is, or None if k is not in the tree
    for i in range(len(T.data)):
        if k.word == T.data[i].word:
            return T.data[i]
    if T.isLeaf:
        return None
    a = SearchBtree(T.child[FindChild(T,k)],k)
    return a

def numberOfNodesBtree(T):
    s = 1
    if not T.isLeaf:
        for c in T.child:
            s += numberOfNodesBtree(c)
    return s

##################HASH TABLES WITH CHAINING FUNCTIONS #########################
    
class HashTableChain(object):
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self,size):  
        self.bucket = [[] for i in range(size)]
        
    def h_length_string(self,k):
        return len(k)%len(self.bucket)

    def h_first_ascii(self,k):
        return ord(k[0])%len(self.bucket)

    def h_product_ascii(self,k):
        return (ord(k[0])*ord(k[-1]))%len(self.bucket)

    def h_sum_ascii(self,k):
        sum1 = 0
        for c in k:
            sum1 += ord(c)
        return sum1%len(self.bucket)

    def h_recursive(self,k):
        if len(k) == 0:
            return 1
        a = (ord(k[0]) + 255 * self.h_recursive(k[1:]))%len(self.bucket)
        return a

    def ascii_times_prime(self,k):
        return (ord(k[0]) * 3) % len(self.bucket) 
            
            
    def insert(self,k, choice):
        # Inserts k in appropriate bucket (list) 
        # Does nothing if k is already in the table
        if choice == '1':
            b = self.h_length_string(k.word)
        elif choice == '2':
            b = self.h_first_ascii(k.word)            
        elif choice == '3':
            b = self.h_product_ascii(k.word)
        elif choice == '4':
            b = self.h_sum_ascii(k.word)
        elif choice == '5':
            b = self.h_recursive(k.word)
        else:
            b = self.ascii_times_prime(k.word)
        if not k in self.bucket[b]:
            self.bucket[b].append(k)         #Insert new item at the end
            
    def find(self,k, choice):
        # Returns bucket (b) and index (i) 
        # If k is not in table, i == -1
        if choice == '1':
            b = self.h_length_string(k)
        elif choice == '2':
            b = self.h_first_ascii(k)            
        elif choice == '3':
            b = self.h_product_ascii(k)
        elif choice == '4':
            b = self.h_sum_ascii(k)
        elif choice == '5':
            b = self.h_recursive(k)
        else:
            b = self.ascii_times_prime(k)
        try:
            i = -1
            for j in range(len(self.bucket[b])):
                if self.bucket[b][j].word == k:
                    i = j
                    break
        except:
            i = -1
        return b, i
     
    def print_table(self):
        print('Table contents:')
        for b in self.bucket:
            print('[', end = '')
            for i in b:
                print(' ', i.word, end = ',')
            print(']')
                
    def load_factor(self):
        counter = 0
        for b in self.bucket:
            counter += len(b)
        return counter / len(self.bucket)

##################HASH TABLES WITH LINEAR PROBING FUNCTIONS ###################
        
class HashTableLP(object):
    # Builds a hash table of size 'size', initilizes items to a WordEmbedding object that has its word initialized to -1 (which means empty)
    # Constructor
    def __init__(self,size):  
        self.item = [WordEmbedding('-1') for x in range(size)]
        
    def h_length_string(self,k, i):
        #Uses the length of the word to hash the WordEmbedding object.
        return ((len(k)+i)%len(self.item))

    def h_first_ascii(self,k, i):
        #Uses the first ascii value of the word to hash the WordEmbedding object.
        return (ord(k[0])+i)%len(self.item)

    def h_product_ascii(self,k, i):
        #Uses the first and last ascii values of the word to hash the WordEmbedding object.
        return ((ord(k[0])*ord(k[-1]))+i)%len(self.item)

    def h_sum_ascii(self,k, i):
        #Sums all ascii values of the characters in the word to hash the WordEmbedding object.
        sum1 = i
        for c in k:
            sum1 += ord(c)
        return sum1%len(self.item)

    def h_recursive(self,k, i):
        #Recursively calculates a hash value for the WordEmbedding object.
        if len(k) == 0:
            return 1
        a = ((ord(k[0]) + 255 * self.h_recursive(k[1:], i)) + i)%len(self.item)
        return a

    def ascii_times_prime(self,k, i):
        #Multiplies the first ascii value of the word times a prime number to hash the WordEmbedding object.
        return ((ord(k[0]) * 3)+i) % len(self.item)
        
    def insert(self,k, choice):
        # Inserts k in table unless table is full
        # Returns the position of k in self, or -1 if k could not be inserted
        #Choice dictates which hash function to use.
        if choice == '1':
            for i in range(len(self.item)): #Despite for loop, running time should be constant for table with low load factor
                pos = self.h_length_string(k.word, i)
                if self.item[pos].word == '-1' or self.item[pos].word == '2':
                    self.item[pos] = k
                    return pos
            return -1
        elif choice == '2':
            for i in range(len(self.item)): #Despite for loop, running time should be constant for table with low load factor
                pos = self.h_first_ascii(k.word, i)
                if self.item[pos].word == '-1' or self.item[pos].word == '2':
                    self.item[pos] = k
                    return pos
            return -1
        elif choice == '3':
            for i in range(len(self.item)): #Despite for loop, running time should be constant for table with low load factor
                pos = self.h_product_ascii(k.word, i)
                if self.item[pos].word == '-1' or self.item[pos].word == '2':
                    self.item[pos] = k
                    return pos
            return -1
        elif choice == '4': 
            for i in range(len(self.item)): #Despite for loop, running time should be constant for table with low load factor
                pos = self.h_sum_ascii(k.word, i)
                if self.item[pos].word == '-1' or self.item[pos].word == '2':
                    self.item[pos] = k
                    return pos
            return -1            
        elif choice == '5':
            for i in range(len(self.item)): #Despite for loop, running time should be constant for table with low load factor
                pos = self.h_recursive(k.word, i)
                if self.item[pos].word == '-1' or self.item[pos].word == '2':
                    self.item[pos] = k
                    return pos
            return -1           
        else:
            for i in range(len(self.item)): #Despite for loop, running time should be constant for table with low load factor
                pos = self.ascii_times_prime(k.word, i)
                if self.item[pos].word == '-1' or self.item[pos].word == '2':
                    self.item[pos] = k
                    return pos
            return -1
    
    def find(self,k, choice):
        # Returns the position of k in table, or -1 if k is not in the table
        #choice dictates which hash function to use for hashing.
        if choice == '1':
            for i in range(len(self.item)):
                pos = self.h_length_string(k.word, i)
                if self.item[pos].word == k.word:
                    return pos
                if self.item[pos] == '-1':
                    return -1
        elif choice == '2':
            for i in range(len(self.item)):
                pos = self.h_first_ascii(k.word, i)
                if self.item[pos].word == k.word:
                    return pos
                if self.item[pos] == '-1':
                    return -1
        elif choice == '3':
            for i in range(len(self.item)):
                pos = self.h_product_ascii(k.word, i)
                if self.item[pos].word == k.word:
                    return pos
                if self.item[pos] == '-1':
                    return -1
        elif choice == '4':
            for i in range(len(self.item)):
                pos = self.h_sum_ascii(k.word, i)
                if self.item[pos].word == k.word:
                    return pos
                if self.item[pos] == '-1':
                    return -1
        elif choice == '5':
            for i in range(len(self.item)):
                pos = self.h_recursive(k.word, i)
                if self.item[pos].word == k.word:
                    return pos
                if self.item[pos] == '-1':
                    return -1
        else:
            for i in range(len(self.item)):
                pos = self.ascii_times_prime(k.word, i)
                if self.item[pos].word == k.word:
                    return pos
                if self.item[pos] == '-1':
                    return -1
    
    def print_table(self):
        print('Table contents:')
        for i in self.item:
            print(i.word)
            
    def loadFactor(self):
        count = 0
        for i in self.item:
            if i.word != '-1':
                if i.word != '-2':
                    count += 1
        return count / len(self.item)
    
#################Text-To-Tree Functions and Similarity Functions###############

#findSimilarities takes two words and the choice of 1 or 2 to indicate to the
#method which option is being used. The distinction is important because searchbst
#returns a node and thus, the data must be accessed and passed. searchBtree returns
#the actual wordembedding object itself so we can access its embedding directly.
def findSimilarities(a, b, choice):
    dotproduct = 0
    magnitudea = 0
    magnitudeb = 0
    similarity = 0
    similarities = []
    if choice == '1':
        dotproduct = np.dot(a.data.emb, b.data.emb)
        magnitudea = np.linalg.norm(a.data.emb)
        magnitudeb = np.linalg.norm(b.data.emb)
        similarity = round((dotproduct)/(magnitudea*magnitudeb), 4) 
        similarities += [[line[0], line[1], similarity]]
    else:
        dotproduct = np.dot(a.emb, b.emb)
        magnitudea = np.linalg.norm(a.emb)
        magnitudeb = np.linalg.norm(b.emb)
        similarity = round((dotproduct)/(magnitudea*magnitudeb), 4)
        similarities += [[line[0], line[1], similarity]]
    return similarities
  
    
class WordEmbedding(object):
    def __init__(self,word,embedding=[]):
        # word must be a string, embedding can be a list or and array of ints or floats
        self.word = word
        self.emb = np.array(embedding, dtype=np.float32) # For Lab 4, len(embedding=50)

#in the main it uses a while loop to continuously run.
if __name__ == "__main__":  
    next_loop = False
    while not next_loop:
        userinput = input('Choose table implementation \nType 1 for binary search tree, 2 for B-Tree, 3 for Hash Tables with Chaining and 4 for Hash Tables with Linear Probing: \n')
        if userinput == '1':
            #if userinput is 1, we run the bstree module.
            print('Choice: 1')
            print()
            print('Building binary search tree')
            print()
            filepath = 'glove.6B.50d.txt'
            A = None
            T = None
            #We start the timer here for bstree construction. The with open
            #chunk of code opens the file and uses a for loop to iterate through the
            #lines of the txt file.
            start1 = time.time()
            with open(filepath, encoding = 'utf-8-sig') as fp:
                for line in fp:
                    line = line.split(' ')
                    #this if statement makes it so we ignore any non-alphabetical
                    #words
                    if len(line[0]) != 0:
                        if ((ord(line[0][0]) < 65) or (ord(line[0][0]) > 90 and ord(line[0][0]) < 97) or (ord(line[0][0]) > 122)):
                            continue
                    #we create a wordembedding out of the line and insert to the tree.
                    A = WordEmbedding(line[0], line[1:])
                    T = InsertBST(T, A)
            end1 = time.time()
            print()
            try:
                #this try block compares the similarities.
                filepath = input('Please enter the filename associated with the words you want similarities for: ')
                print('Building binary search tree done.')
                print('Beginning query processing.')
                similarities = []
                skip = False
                start = time.time()
                #We open the file that contains the pairs of words and for each line
                #search for the words in the BSTree we created earlier.
                with open(filepath, encoding = 'utf-8-sig') as fp:
                    for line in fp:
                        line = line.strip().split(' ')
                        if len(line[0]) == 0 or len (line[1]) == 0:
                            print('txt file containing words that similarities are being requested for does not seem to be formatted appropriately.')
                            skip = True
                            break
                        a = searchBST(T, line[0])
                        b = searchBST(T, line[1])
                        #we then store the similarities of the line.
                        similarities += findSimilarities(a, b, userinput)
                end = time.time()
                if not skip:
                    #Here we print out all our stats. We ask the user to see
                    #if they want us to print out the similarities in the scenario
                    #we are running a very large number of similarities.
                    print()
                    print('Binary Search Tree stats:')
                    print('Number of nodes: ', numberOfNodes(T))
                    print('Height: ', heightBST(T))
                    print()
                    print('Reading word file to determine similarities.')
                    print('Running time for binary search tree query processing: ', round((end-start), 4), ' seconds.')
                    print('Running time for binary search tree construction: ', round((end1-start1), 4), ' seconds.')
                    if len(similarities) > 0:
                        z = input('Print similarities? (Y/N): ')
                        print()
                        if z.lower() == 'y':
                            print('Following Similarities Found:')
                            for s in similarities:
                                print('[', s[0], ',', s[1],'] = ', s[2])
                    else:
                        print('No similarities found.')
            except:
                print('File not found.')
        elif userinput == '2':
            #Choice 2 runs the btree.
            print('Choice: 2')
            maxD = int(input('Maximum number of items in node: '))
            skip = False
            print()
            print('Building B-tree')
            print()
            filepath = 'glove.6B.50d.txt'
            A = None
            #We create a Btree with the max data recovered from the user.
            T = BTree([], max_data=maxD)
            similarities = []
            startT = time.time()
            #We do the same as in the BST; we read line by line, convert the line
            #into a wordembedding object, and insert that object into the btree.
            with open(filepath, encoding = 'utf-8-sig') as fp:
                for line in fp:
                    line = line.split(' ')
                    if len(line[0]) != 0:
                        if ((ord(line[0][0]) < 65) or (ord(line[0][0]) > 90 and ord(line[0][0]) < 97) or (ord(line[0][0]) > 122)):
                            continue
                    A = WordEmbedding(line[0], line[1:])
                    InsertBtree(T, A)
            endT = time.time()
            print()
            print('Reading word file to determine similarities.')
            print()
            try:
                #We then ask the user for the txt file that contains the pairs of words.
                filepath = input('Please enter the filename associated with the words you want similarities for: ')
                print('Reading word file to determine similarities.')
                startA = time.time()
                #we read the pairs of words line by line and create wordembedding objects
                #from them (with an empty emb) since I modified the btree methods to work specifically only
                #with wordembedding objects.
                #we then search for those objects in the btree and return the actual object.
                with open(filepath, encoding = 'utf-8-sig') as fp:
                    for line in fp:
                        line = line.strip().split(' ')
                        if len(line[0]) == 0 or len (line[1]) == 0:
                            print('txt file containing words that similarities are being requested for does not seem to be formatted appropriately.')
                            skip = True
                            break
                        word1 = WordEmbedding(line[0])
                        word2 = WordEmbedding(line[1])
                        st = time.time_ns()
                        a = SearchBtree(T, word1)
                        b = SearchBtree(T, word2)
                        st = time.time_ns()
                        #we save the similarities here.
                        similarities += findSimilarities(a,b, userinput)
                endA = time.time()
                if not skip:
                    #we print out the stats for the btree.
                    print()
                    print('BTree stats:')
                    print('Number of nodes: ', numberOfNodesBtree(T))
                    print('Height: ', HeightBtree(T))
                    print()
                    print('Running time for btree query processing: ', round((endA-startA), 4), ' seconds.')
                    print('Running time for btree construction: ', round((endT-startT), 4), ' seconds.')
                    if len(similarities) > 0:
                        z = input('Print similarities? (Y/N): ')
                        print()
                        if z.lower() == 'y':
                            print('Following Similarities Found:')
                            for s in similarities:
                                print('[', s[0], ',', s[1],'] = ', s[2])
                    else:
                        print('No similarities found.')
            except:
                print('File not found.')
        elif userinput == '3':
            #if userinput is 3, we run the hash table with chaining module.
            print('Choice: 3')
            print()
            print('which of the following hash functions would you like to use?')
            choiceloop = False
            choice = ''
            while not choiceloop: 
                choice = input('1 = length of string; 2 = ascii value; 3 = product of ascii values; 4 = sum of ascii values; 5 = recursive; 6 = first ascii value squared: ')
                if choice == '1' or choice == '2' or choice == '3' or choice == '4' or choice =='5' or choice == '6':
                    choiceloop = True
            print('Building Hash Table with Chaining with hash table choice ', choice)
            print()
            filepath = 'glove.6B.50d.txt'
            #Here we count the number of lines in the filepath to use this as the size of the hashtable.
            counter = 0
            with open(filepath, encoding = 'utf-8-sig') as fp:
                for line in fp:
                    counter += 1
            counter = int(counter * 1.1)
            print('The hash table will have a length of ',counter)
            htc = HashTableChain(counter)
            A = None
            #We start the timer here for hash table construction. The with open
            #chunk of code opens the file and uses a for loop to iterate through the
            #lines of the txt file.
            start1 = time.time()
            with open(filepath, encoding = 'utf-8-sig') as fp:
                for line in fp:
                    line = line.split(' ')
                    #this if statement makes it so we ignore any non-alphabetical
                    #words
                    if len(line[0]) != 0:
                        if ((ord(line[0][0]) < 65) or (ord(line[0][0]) > 90 and ord(line[0][0]) < 97) or (ord(line[0][0]) > 122)):
                            continue
                    #we create a wordembedding out of the line and insert to the hash table.
                    A = WordEmbedding(line[0], line[1:])
                    htc.insert(A, choice)
            end1 = time.time()
            print()
            print('building hash table with chaining done')
            try:
                    #this try block compares the similarities.
                filepath = input('Please enter the filename associated with the words you want similarities for: ')
                print('Beginning query processing.')
                similarities = []
                skip = False
                start = time.time()
                #We open the file that contains the pairs of words and for each line
                #search for the words in the BSTree we created earlier.
                with open(filepath, encoding = 'utf-8-sig') as fp:
                    for line in fp:
                        line = line.strip().split(' ')
                        if len(line[0]) == 0 or len (line[1]) == 0:
                            print('txt file containing words that similarities are being requested for does not seem to be formatted appropriately.')
                            skip = True
                            break
                        b1, i1 = htc.find(line[0], choice)
                        b2, i2 = htc.find(line[1], choice)
                        #we then store the similarities of the line.
                        similarities += findSimilarities(htc.bucket[b1][i1], htc.bucket[b2][i2], userinput)
                end = time.time()
                if not skip:
                    #Here we print out all our stats. We ask the user to see
                    #if they want us to print out the similarities in the scenario
                    #we are running a very large number of similarities.
                    print()
                    print('Hash Table With Chaining stats:')
                    print('Size of Table: ', len(htc.bucket))
                    print('Load Factor: ', htc.load_factor())
                    print()
                    print('Reading word file to determine similarities.')
                    print('Running time for hash table with chaining query processing: ', round((end-start), 4), ' seconds.')
                    print('Running time for hash table with chaining construction: ', round((end1-start1), 4), ' seconds.')
                    if len(similarities) > 0:
                        z = input('Print similarities? (Y/N): ')
                        print()
                        if z.lower() == 'y':
                            print('Following Similarities Found:')
                            for s in similarities:
                                print('[', s[0], ',', s[1],'] = ', s[2])
                    else:
                        print('No similarities found.')
            except:
                print('File not found.')
           
        elif userinput == '4':
            #if userinput is 4, we run the hash table with linear probing module.
            print('Choice: 4')
            print()
            print('which of the following hash functions would you like to use?')
            choiceloop = False
            choice = ''
            while not choiceloop: 
                choice = input('1 = length of string; 2 = ascii value; 3 = product of ascii values; 4 = sum of ascii values; 5 = recursive; 6 = first ascii value squared: ')
                if choice == '1' or choice == '2' or choice == '3' or choice == '4' or choice =='5' or choice == '6':
                    choiceloop = True
            print('Building Hash Table with Linear Probing with hash table choice ', choice)
            print()
            filepath = 'glove.6B.50d.txt'
            #Here we count the number of lines in the filepath to use this as the size of the hashtable.
            counter = 0
            with open(filepath, encoding = 'utf-8-sig') as fp:
                for line in fp:
                    counter += 1
            counter = int(counter * 1.1)
            print('The hash table will have a length of ',counter)
            htlp = HashTableLP(counter)
            #We start the timer here for hash table construction. The with open
            #chunk of code opens the file and uses a for loop to iterate through the
            #lines of the txt file.
            start1 = time.time()
            with open(filepath, encoding = 'utf-8-sig') as fp:
                for line in fp:
                    line = line.split(' ')
                    #this if statement makes it so we ignore any non-alphabetical
                    #words
                    if len(line[0]) != 0:
                        if ((ord(line[0][0]) < 65) or (ord(line[0][0]) > 90 and ord(line[0][0]) < 97) or (ord(line[0][0]) > 122)):
                            continue
                    #we create a wordembedding out of the line and insert to the hash table.
                    A = WordEmbedding(line[0], line[1:])
                    htlp.insert(A, choice)
            end1 = time.time()
            print()
            htlp.print_table()
            print('building hash table with linear probing done')
            try:
                    #this try block compares the similarities.
                filepath = input('Please enter the filename associated with the words you want similarities for: ')
                print('Beginning query processing.')
                similarities = []
                skip = False
                start = time.time()
                #We open the file that contains the pairs of words and for each line
                #search for the words in the BSTree we created earlier.
                with open(filepath, encoding = 'utf-8-sig') as fp:
                    for line in fp:
                        line = line.strip().split(' ')
                        if len(line[0]) == 0 or len (line[1]) == 0:
                            print('txt file containing words that similarities are being requested for does not seem to be formatted appropriately.')
                            skip = True
                            break
                        item1 = WordEmbedding(line[0])
                        item2 = WordEmbedding(line[1])
                        i1 = htlp.find(item1, choice)
                        i2 = htlp.find(item2, choice)
                        #we then store the similarities of the line.
                        similarities += findSimilarities(htlp.item[i1], htlp.item[i2], userinput)
                end = time.time()
                if not skip:
                    #Here we print out all our stats. We ask the user to see
                    #if they want us to print out the similarities in the scenario
                    #we are running a very large number of similarities.
                    print()
                    print('Hash Table With Linear Probing stats:')
                    print('Size of Table: ', len(htlp.item))
                    print('Load Factor: ', htlp.loadFactor())
                    print()
                    print('Reading word file to determine similarities.')
                    print('Running time for hash table with chaining query processing: ', round((end-start), 4), ' seconds.')
                    print('Running time for hash table with chaining construction: ', round((end1-start1), 4), ' seconds.')
                    if len(similarities) > 0:
                        z = input('Print similarities? (Y/N): ')
                        print()
                        if z.lower() == 'y':
                            print('Following Similarities Found:')
                            for s in similarities:
                                print('[', s[0], ',', s[1],'] = ', s[2])
                    else:
                        print('No similarities found.')
            except:
                print('File not found.')
        else:
            next_loop = True