# Edge list representation of graphs
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import graph_AL as g_AL
import graph_AM as g_AM

class Edge:
    def __init__(self, source, dest, weight=1):
        self.source = source
        self.dest = dest
        self.weight = weight
        
class Graph:
    # Constructor
    def __init__(self,  vertices, weighted=False, directed = False):
        self.vertices = vertices
        self.el = []
        self.weighted = weighted
        self.directed = directed
        self.representation = 'EL'
        
    def BFS(self):
        frontierQ = []
        discovered = []
        path = []
        for v in range(self.vertices): 
            discovered.append(False) #We populate the discovered list with False for every vertex
            path.append(-1) #we populate the path list with -1's for every vertex
        frontierQ.append(0)# we push the starting vertex 0 to the frontier.
        discovered[0] = True #We acknowledge vertex 0 as discovered.
        while (len(frontierQ) > 0):
            currentV = frontierQ.pop(0)
            for edge in self.el: #We must loop through the edges in order to find the ones adjacent to currentV.
                if edge.source == currentV: #Since the edges in an edge list are only added once, we must check to see if the currentV is the source or the destination at the edge we are checking.
                    if not discovered[edge.dest]:
                        frontierQ.append(edge.dest)
                        discovered[edge.dest] = True
                        path[edge.dest] = currentV
                if edge.dest == currentV:
                    if not discovered[edge.source]:
                        frontierQ.append(edge.source)
                        discovered[edge.source] = True
                        path[edge.source] = currentV
        a = returnPath(path, 15)
        return a
    
    
    ##DFS is the same as BFS but we changed the queue for a stack.
    def DFS(self):
        stack = []
        discovered = []
        path = []
        for v in range(self.vertices):
            discovered.append(False) #We populate the discovered list with False for every vertex
            path.append(-1) #we populate the path list with -1's for every vertex
        stack.append(0) # we push the starting vertex 0 to the stack.
        discovered[0] = True #We acknowledge vertex 0 as discovered.
        while (len(stack) > 0):
            currentV = stack.pop(0)
            for edge in self.el:
                if edge.source == currentV:
                    if not discovered[edge.dest]:
                        stack.insert(0, edge.dest)
                        discovered[edge.dest] = True
                        path[edge.dest] = currentV
                if edge.dest == currentV:
                    if not discovered[edge.source]:
                        stack.insert(0, edge.source)
                        discovered[edge.source] = True
                        path[edge.source] = currentV
        a = returnPath(path, 15)
        return a
        
    def insert_edge(self,source,dest,weight=1):
        temp_edge = Edge(source, dest, weight)
        match = False
        if self.directed:
            for edge in self.el:
                if (edge.source == temp_edge.source and edge.dest == temp_edge.dest):
                    match = True
                    break
            if not match:
                self.el.append(temp_edge)
                self.el.sort(key = lambda edge: edge.source)
            
        else:
            for edge in self.el:
                if (edge.source == temp_edge.source and edge.dest == temp_edge.dest) or (edge.source == temp_edge.dest and edge.dest == temp_edge.source):
                    match = True
                    break
            if not match:
                self.el.append(temp_edge)
                self.el.sort(key = lambda edge: edge.source)
                
    def delete_edge(self,source,dest):
        counter = 0
        if self.directed:
            for edge in self.el:
                if edge.source == source and edge.dest == dest:
                    break
                counter += 1
        else:
            for edge in self.el:
                if (edge.source == source and edge.dest == dest) or (edge.source == dest and edge.dest == source):
                    break
                counter += 1
        del self.el[counter]
            
                
    def display(self):
        print('[', end = '')
        for e in self.el:
            print('(',e.source, ',', e.dest, ',', e.weight, ')', end = '')
        print(']')
     
    def draw(self):
        g = self.as_AM()
        g.draw()

            
    def as_EL(self):
        return self
    
    def as_AM(self):
        g = g_AM.Graph(self.vertices, self.weighted, self.directed)
        for edge in self.el:
            g.insert_edge(edge.source, edge.dest, edge.weight)
        return g
    
    def as_AL(self):
        g = g_AL.Graph(self.vertices, self.weighted, self.directed)
        for edge in self.el:
            g.insert_edge(edge.source, edge.dest, edge.weight)
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