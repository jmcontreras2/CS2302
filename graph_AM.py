# Adjacency matrix representation of graphs
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import graph_AL as g_AL
import graph_EL as g_EL

class Graph:
    # Constructor
    def __init__(self, vertices, weighted=False, directed = False):
        self.am = np.zeros((vertices,vertices),dtype=int) - 1
        self.weighted = weighted
        self.directed = directed
        self.representation = 'AM'
        
    def BFS(self):
        frontierQ = []
        discovered = []
        path = []
        for v in range(self.am.shape[0]):
            discovered.append(False) #We populate the discovered list with False for every vertex
            path.append(-1) #we populate the path list with -1's for every vertex
        frontierQ.append(0) #We acknowledge vertex 0 as discovered.
        discovered[0] = True
        while (len(frontierQ) > 0):
            currentV = frontierQ.pop(0)
            for adjV in range(self.am.shape[1]): #We loop through the adjacent vertices in the AM by looping through the row corresponding to currentV and looking to see if the weight is not -1. If not, we identify it as adjacent.
                if self.am[currentV][adjV] != -1:
                    if not discovered[adjV]:
                        frontierQ.append(adjV)
                        discovered[adjV] = True
                        path[adjV] = currentV
        a = returnPath(path, 15)
        return a
    
    #DFS is the same as BFS but with a stack instead of a queue.
    def DFS(self):
        stack = []
        discovered = []
        path = []
        for v in range(self.am.shape[0]):
            discovered.append(False)
            path.append(-1)
        stack.append(0)
        discovered[0] = True
        while (len(stack) > 0):
            currentV = stack.pop(0)
            for adjV in range(self.am.shape[1]):
                if self.am[currentV][adjV] != -1:
                    if not discovered[adjV]:
                        stack.insert(0, adjV)
                        discovered[adjV] = True
                        path[adjV] = currentV
        a = returnPath(path, 15)
        return a
        
    def insert_edge(self,source,dest,weight=1):
        if self.directed:
            self.am[source][dest] = weight
        else:
            self.am[source][dest] = weight
            self.am[dest][source] = weight
        
    def delete_edge(self,source,dest): #assumes -1 is indicative of no edge.
        if self.directed:
            self.am[source][dest] = -1 
        else:
            self.am[source][dest] = -1
            self.am[dest][source] = -1
                
    def display(self):
        print(self.am)
     
    def draw(self):
        g = self.as_AL()
        g.draw()
    
    def as_EL(self):
        g = g_EL.Graph(self.am.shape[0], weighted = self.weighted, directed = self.directed)
        if self.directed: 
            for i in range(self.am.shape[0]):
                for j in range(self.am.shape[1]):
                    if self.am[i][j] != -1:
                        g.insert_edge(i, j, self.am[i][j])
                        g.el.sort(key = lambda edge: edge.source)
        else:
            for i in range(self.am.shape[0]):
                for j in range(i, self.am.shape[1]):
                    if self.am[i][j] != -1:
                        g.insert_edge(i, j, self.am[i][j])
        return g
    
    def as_AM(self):
        return self
    
    def as_AL(self):
        g = g_AL.Graph(self.am.shape[0], weighted = self.weighted, directed = self.directed)
        if self.directed:
            for i in range(self.am.shape[0]):
                for j in range(self.am.shape[1]):
                    if self.am[i][j] != -1:
                        g.insert_edge(i, j, self.am[i][j])
        else:
            for i in range(self.am.shape[0]):
                for j in range(i, self.am.shape[1]):
                    if self.am[i][j] != -1:
                        g.insert_edge(i, j, self.am[i][j])
                        g.insert_edge(j, i, self.am[i][j])
        return g
    
def printPath(path, dest):
    if path[dest] != -1:
        printPath(path, path[dest])
        print(' ', dest)
    else:
        print(' ', dest)

def returnPath(path, dest):
    L = []
    if path[dest] != -1:
        L += returnPath(path, path[dest])
        L.append(dest)
    else:
        L.append(dest)
    return L