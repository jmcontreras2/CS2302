#CS2302 Fall 2019 MW 10:30 A.M. - 11:50 A.M
#Author: Jonatan M. Contreras
#Assignment: Lab 7 - Graphs
#Instructor: Dr. Olac Fuentes
#TA: PhD Student Anindita Nath
#Peer Leader: Diego Rodriguez
#Date of Last Modification: 12/3/2019

#Purpose of Program: The purpose of this program is to implement three algorithm design techniques:
#randomization; backtracking; and dynamic programming. For the randomization algorithm, a hamiltonian cycle
#is tested for for a maximum number of trials. For the backtracking algorithm, the algorithm used in the
#randomized algorithm for hamiltonian cycles is adapted to be a backtracking algorithm (based on the subset
#problem code). Finally, the edit distance algorithm is changed in order to only allow replacement when
#both letters are vowels or consonants.

import numpy as np
import random
import graph_AL as graph
import graph_EL as g_EL
import connected_components as cc
import time

#####################METHODS FOR RANDOMIZED HAMILTONIAN CYCLE ALGORITHM#############################
#This is a helper method for the randomized hamiltonian algorithm in order to grab a subset of e edges of size v.
def random_subset(v, e):
    edges = []
    while len(edges) < v:
        edge = random.randint(0, len(e)-1)
        edges.append(e[edge])
    return edges

#This is a helper method to transform an EL representation graph into a variable containing the vertices and a variable containing the edges.
def g_transform(G):
    v = G.vertices
    e = G.el
    return v, e

#This is the main method. It calls the transform helper method to then send v and e to the main helper method that finds a randomized hamiltonian cycle.
def randomized_hamiltonian(G, max_trials):
    v, e = g_transform(G)
    return randomized_hamiltonian_(v, e, max_trials)
    
#This is the main helper method that finds the randomized hamiltonian cycle. It collects a random subset
# of v edges, creates a graph out of this subset, and finds the connected component as well as checks the
#in_degree of every vertex to make sure it is two. If there is only one connected compontent and an in degre
# of 2 for every vertex, then the method returns the subset of edges. Else, it continues for the 
#set amount of trials. If it doesn't find one within these trials, it returns None.
def randomized_hamiltonian_(v, e, max_trials):
    for i in range(max_trials):
        Eh = random_subset(v, e)
        potential = graph.Graph(v)
        in_degree_2 = True
        for edge in Eh:
            potential.insert_edge(edge.source, edge.dest, edge.weight)
        potential_cc = cc.connected_components(potential)
        for vertex in range(len(potential.al)):
            if potential.in_degree(vertex) != 2:
                in_degree_2 = False
        if potential_cc[0] == 1 and in_degree_2 == True:
            return Eh
    return None  

##########################METHODS FOR BACKTRACKING HAMILTONIAN CYCLE ALGORITHM###############################

#This is a helper method that checks an edge list for a hamiltonian cycle. It is based on the randomized
#hamiltonian cycle algorithm but it only runs for one set of edges.
def hc_check(v, e):
    potential = g_EL.Graph(v)
    in_degree_2 = True
    for edge in e:
        potential.insert_edge(edge.source, edge.dest, edge.weight)
    potential = potential.as_AL()
    potential_cc = cc.connected_components(potential)
    for vertex in range(len(potential.al)):
        if potential.in_degree(vertex) != 2:
            in_degree_2 = False
    if potential_cc[0] == 1 and in_degree_2 == True:
        return e
    return None

#This is the backtrack algorithm. I used the subset problem backtracking algorithm as a base and 
#altered it to work for sets of edges. Its base case is when the length of the subset of edges being tested
#for a hamiltonian cycle is the size of v, which is a prerequisite for the hamiltonian cycle. If this is the case
#, hc_check checks for a hamiltonian cycle. If one exists, it returns it.
    
#If the base case is not executed, we take the first edge in the first recursion call. It does this until
# Eh is of length v. The second recursion call explores the possibility of not selecting the first edge
#for the edge list. It finalizes by returning potential, and if it never found a hamiltonian cycle, it 
#will return None.
def hc_backtrack(v, e, Eh):
    if len(Eh) == v:
        return hc_check(v, Eh)
    if len(e) < 1:
        return None
    potential = hc_backtrack(v, e[1:], Eh + [e[0]])
    if potential is not None:
        return potential
    potential = hc_backtrack(v, e[1:], Eh)
    return potential


#############################DYNAMIC PROGRAMMING EDIT DISTANCE METHOD ##############################

#In the edit distance function, if the cost is taken from a diagonal, this means the letter was replaced.
#Since we are limiting replacements to only when both letters are vowels or consonants, we must limit
#taking from this cost. Thus, I make a list of vowels and when the letters aren't equal to each other,
# I check to see if both are either in the vowels list or both are not. If both are, or both are not, replacements
#are allowed by taking the min of all three options of costs. Else, we only take the min of 
# insertion and deletion.
def edit_distance(s1,s2):
    d = np.zeros((len(s1)+1,len(s2)+1),dtype=int)
    vowels = ['a', 'e', 'i', 'o', 'u']
    d[0,:] = np.arange(len(s2)+1)
    d[:,0] = np.arange(len(s1)+1)
    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            if s1[i-1] ==s2[j-1]:
                d[i,j] =d[i-1,j-1]
            else:
                n = [d[i,j-1],d[i-1,j-1],d[i-1,j]]
                if (s1[i-1].lower() in vowels and s2[j-1].lower() in vowels) or (s1[i-1].lower() not in vowels and s2[j-1].lower() not in vowels):
                    d[i,j] = min(n)+1      
                else:
                    d[i,j] = min(n[0], n[2]) + 1
    print(d)
    return d[-1,-1]

g = g_EL.Graph(3)
g.insert_edge(0, 1)
g.insert_edge(0, 2)
g.insert_edge(1,2)
el1 = g.el
el2 = []
v = g.vertices
start = time.time()
a = hc_backtrack(v, el1, el2)
end = time.time()
print('first graph hc: easy')
for edge in a:
    print(edge.source, edge.dest, edge.weight)
g = g_EL.Graph(4)
g.insert_edge(0, 1)
g.insert_edge(0, 3)
g.insert_edge(1,2)
g.insert_edge(2,3)
el1 = g.el
el2 = []
v = g.vertices
print('took ', end-start, ' seconds')
start = time.time()
a = hc_backtrack(v, el1, el2)
end = time.time()
print('second graph hc: medium')
if a == None:
    print(a)
else:
    for edge in a:
        print(edge.source, edge.dest, edge.weight)
g = g_EL.Graph(8)
g.insert_edge(0, 1)
g.insert_edge(0, 4)
g.insert_edge(0, 7)
g.insert_edge(1 ,2)
g.insert_edge(1, 5)
g.insert_edge(2, 6)
g.insert_edge(2, 3)
g.insert_edge(3, 7)
g.insert_edge(3, 4)
g.insert_edge(4, 5)
g.insert_edge(5, 6)
g.insert_edge(6, 7)
el1 = g.el
el2 = []
v = g.vertices
print('took ', end-start, ' seconds')
start = time.time()
a = hc_backtrack(v, el1, el2)
end = time.time()
print('third graph hc: hard')
if a == None:
    print(a)
else:
    for edge in a:
        print(edge.source, edge.dest, edge.weight)
g = g_EL.Graph(5)
g.insert_edge(0, 1)
g.insert_edge(0, 4)
g.insert_edge(1, 4)
g.insert_edge(1, 2)
g.insert_edge(1, 3)
g.insert_edge(2, 3)
el1 = g.el
el2 = []
v = g.vertices
print('took ', end-start, ' seconds')
start = time.time()
a = hc_backtrack(v, el1, el2)
end = time.time()
print('fourth graph hc: impossible')
if a == None:
    print(a)
else:
    for edge in a:
        print(edge.source, edge.dest, edge.weight)
print('took ', end-start, ' seconds')
