# Adjacency list representation of graphs
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import graph_AL as g_AL
import graph_AM as g_AM

class Edge:
    def __init__(self, dest, weight=1):
        self.dest = dest
        self.weight = weight
        
class Graph:
    # Constructor
    def __init__(self, vertices, weighted=False, directed = False):
        self.al = [[] for i in range(vertices)]
        self.weighted = weighted
        self.directed = directed
        self.representation = 'AL'
        
    def BFS(self):
        frontierQ = []
        discovered = []
        path = []
        for v in self.al: 
            discovered.append(False) #We populate the discovered list with False for every vertex
            path.append(-1) #we populate the path list with -1's for every vertex
        frontierQ.append(0) # we push the starting vertex 0 to the frontier.
        discovered[0] = True #We acknowledge vertex 0 as discovered.
        while (len(frontierQ) > 0):
            currentV = frontierQ.pop(0)
            for adjV in self.al[currentV]: #We loop through the adjacent vertices to current vertex by looping through its list that contains adjacent vertices.
                    if not discovered[adjV.dest]:
                        frontierQ.append(adjV.dest)
                        discovered[adjV.dest] = True
                        path[adjV.dest] = currentV
        a = returnPath(path, 15)
        return a
    
    
    ##DFS is the same as BFS but with a stack instead of a queue.
    def DFS(self):
        stack = []
        discovered = []
        path = []
        for v in self.al:
            discovered.append(False)
            path.append(-1)
        stack.append(0)
        discovered[0] = True
        while (len(stack) > 0):
            currentV = stack.pop()
            for adjV in self.al[currentV]:
                if not discovered[adjV.dest]:
                    stack.append(adjV.dest)
                    discovered[adjV.dest] = True
                    path[adjV.dest] = currentV
        a = returnPath(path, 15)
        return a
        
    def insert_edge(self,source,dest,weight=1):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            print('Error, vertex number out of range')
        elif weight!=1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.al[source].append(Edge(dest,weight)) 
            self.al[source].sort(key = lambda edge: edge.dest)
            if not self.directed:
                self.al[dest].append(Edge(source,weight))
                self.al[dest].sort(key = lambda edge: edge.dest)
    
    def delete_edge_(self,source,dest):
        i = 0
        for edge in self.al[source]:
            if edge.dest == dest:
                self.al[source].pop(i)
                return True
            i+=1    
        return False
    
    def count_edges(self):
        sum1 = 0
        for i in self.al:
            sum1 += len(i)
        if self.directed == True:
            return sum1
        else:
            return sum1//2
        
    def highest_cost_edge(G):
        hce = [-1, -1, 0]
        for v in range(len(G.al)):
            for edge in G.al[v]:
                if edge.weight>hce[-1]:
                    hce = [v, edge.dest, edge.weight]
        return hce
                    
    
    def delete_edge(self,source,dest):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            print('Error, vertex number out of range')
        else:
            deleted = self.delete_edge_(source,dest)
            if not self.directed:
                deleted = self.delete_edge_(dest,source)
        if not deleted:        
            print('Error, edge to delete not found')      
            
    def display(self):
        print('[',end='')
        for i in range(len(self.al)):
            print('[',end='')
            for edge in self.al[i]:
                print('('+str(edge.dest)+','+str(edge.weight)+')',end='')
            print(']',end=' ')    
        print(']')   
     
    def draw(self):
        scale = 30
        fig, ax = plt.subplots()
        for i in range(len(self.al)):
            for edge in self.al[i]:
                d,w = edge.dest, edge.weight
                if self.directed or d>i:
                    x = np.linspace(i*scale,d*scale)
                    x0 = np.linspace(i*scale,d*scale,num=5)
                    diff = np.abs(d-i)
                    if diff == 1:
                        y0 = [0,0,0,0,0]
                    else:
                        y0 = [0,-6*diff,-8*diff,-6*diff,0]
                    f = interp1d(x0, y0, kind='cubic')
                    y = f(x)
                    s = np.sign(i-d)
                    ax.plot(x,s*y,linewidth=1,color='k')
                    if self.directed:
                        xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                        yd = [y0[2]-1,y0[2],y0[2]+1]
                        yd = [y*s for y in yd]
                        ax.plot(xd,yd,linewidth=1,color='k')
                    if self.weighted:
                        xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                        yd = [y0[2]-1,y0[2],y0[2]+1]
                        yd = [y*s for y in yd]
                        ax.text(xd[2]-s*2,yd[2]+3*s, str(w), size=12,ha="center", va="center")
            ax.plot([i*scale,i*scale],[0,0],linewidth=1,color='k')        
            ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
             bbox=dict(facecolor='w',boxstyle="circle"))
        ax.axis('off') 
        ax.set_aspect(1.0)            
            
    def as_EL(self):
        g = g_AM.Graph(self.vertices, self.weighted, self.directed)
        for list in range(len(self.al)):
            for edge in range(len(self.al[list])):
                g.insert_edge(edge.source, edge.dest, edge.weight)
        return g
    
    def as_AM(self):
        g = g_AM.Graph(self.vertices, self.weighted, self.directed)
        for list in range(len(self.al)):
            for edge in range(len(self.al[list])):
                g.insert_edge(edge.source, edge.dest, edge.weight)                
        return g
    
    def as_AL(self):
        return self
    
def out_degree(G, v):
    if v < len(G.al) and v > -1:
        return len(G.al[v])

def in_degree(G, v):
    count = 0
    for i in G.al:
        for j in i:
            if len(i) != 0:
                if j.dest == v:
                    count += 1
    return count

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