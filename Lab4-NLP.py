#CS2302 Fall 2019 MW 10:30 A.M. - 11:50 A.M
#Author: Jonatan M. Contreras
#Assignment: Lab 4 - NLP Implementation
#Instructor: Dr. Olac Fuentes
#TA: PhD Student Anindita Nath
#Peer Leader: Diego Rodriguez
#Date of Last Modification: 10/14/2019

#Purpose of Program: The program asks the user to choose an implementation out of the
#choices of BSTree and BTree. If BTree, the program also asks the user to select max_data for each node.
#The program then builds a BSTree or BTree out of the words in the file glove.6B.50d.txt, skipping
#any punctuation marks or words that don't begin with an alphabetical character. Once these are stored,
#the program asks the user to input the name of a .txt file with words to compare. It finishes by asking
#the user if they want the similarities printed, as large numbers of similarities were calculated for 
#testing purposes.

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
        userinput = input('Choose table implementation \nType 1 for binary search tree or 2 for B-Tree: \n')
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
        else:
            next_loop = True