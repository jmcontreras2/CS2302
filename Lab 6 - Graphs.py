#CS2302 Fall 2019 MW 10:30 A.M. - 11:50 A.M
#Author: Jonatan M. Contreras
#Assignment: Lab 6 - Graphs
#Instructor: Dr. Olac Fuentes
#TA: PhD Student Anindita Nath
#Peer Leader: Diego Rodriguez
#Date of Last Modification: 11/17/2019

#Purpose of Program: The purpose of this program is to solve the fox-chicken-grain
#riddle using graphs. The graph representing the world is implemented using three
#different representations of graphs and two unique solutions are discovered
#using breadth-first-search and depth-first-search. 

import matplotlib.pyplot as plt
import numpy as np
import graph_AL as g_AL
import graph_AM as g_AM 
import graph_EL as g_EL
import time

#Solving Puzzle using Edge List Representation; we first create the graph and insert
#legal transition edges into the graph, connecting only legal states with legal
#transitions.

g = g_EL.Graph(16)
g.insert_edge(0, 5, 1)
g.insert_edge(2, 7, 1)
g.insert_edge(2, 11, 1)
g.insert_edge(4, 5, 1)
g.insert_edge(4, 7, 1)
g.insert_edge(4, 13, 1)
g.insert_edge(8, 13, 1)
g.insert_edge(8, 11, 1)
g.insert_edge(10, 15, 1)
g.insert_edge(10, 11, 1)
g.draw()
print('Edge List Representation of Graph')
print()
g.display()
print()
start = time.time()
p = g.BFS()
end = time.time()
print('Edge List BFS Solution')
print('To solve the puzzle, you must first travel from world state ', end = '')
for state in range(len(p)-1):
    print(p[state], ' to ', end = ' ')
print(p[-1])
print('Runtime for BFS: ', end-start)
print()
print('Edge List DFS Solution')
start = time.time()
p = g.DFS()
end = time.time()
print('To solve the puzzle, you must first travel from world state ', end = '')
for state in range(len(p)-1):
    print(p[state], ' to ', end = ' ')
print(p[-1])
print('Runtime for DFS: ', end-start)
print()

#Solving Puzzle using Adjacency Matrix Representation; we first create the graph and insert
#legal transition edges into the graph, connecting only legal states with legal
#transitions.

print('Adjacency Matrix Representation of Graph')
print()
g = g_AM.Graph(16)
g.insert_edge(0, 5, 1)
g.insert_edge(2, 7, 1)
g.insert_edge(2, 11, 1)
g.insert_edge(4, 13, 1)
g.insert_edge(4, 7, 1)
g.insert_edge(4, 5, 1)
g.insert_edge(8, 13, 1)
g.insert_edge(8, 11, 1)
g.insert_edge(10, 15, 1)
g.insert_edge(10, 11, 1)
g.draw()
g.display()
start = time.time()
p = g.BFS()
end = time.time()
print()

print('Adjacency Matrix BFS Solution')
print()
print('To solve the puzzle, you must first travel from world state ', end = '')
for state in range(len(p)-1):
    print(p[state], ' to ', end = ' ')
print(p[-1])
print('Runtime for BFS: ', end-start)
print()

start = time.time()
p = g.DFS()
end = time.time()
print('Adjacency Matrix DFS Solution')
print()
print('To solve the puzzle, you must first travel from world state ', end = '')
for state in range(len(p)-1):
    print(p[state], ' to ', end = ' ')
print(p[-1])
print('Runtime for DFS: ', end-start)
print()

#Solving Puzzle using Adjacency List Representation; we first create the graph and insert
#legal transition edges into the graph, connecting only legal states with legal
#transitions.
print('Adjacency List Representation of Graph')
print()
g = g_AL.Graph(16)
g.insert_edge(0, 5, 1)
g.insert_edge(2, 7, 1)
g.insert_edge(2, 11, 1)
g.insert_edge(4, 13, 1)
g.insert_edge(4, 7, 1)
g.insert_edge(4, 5, 1)
g.insert_edge(8, 13, 1)
g.insert_edge(8, 11, 1)
g.insert_edge(10, 15, 1)
g.insert_edge(10, 11, 1)
g.draw()
g.display()
start = time.time()
p = g.BFS()
end = time.time()
print()

print('Adjacency List BFS Solution')
print()
print('To solve the puzzle, you must first travel from world state ', end = '')
for state in range(len(p)-1):
    print(p[state], ' to ', end = ' ')
print(p[-1])
print('Runtime for BFS: ', end-start)
print()
start = time.time()
p = g.DFS()
end = time.time()
print('Adjacency List DFS Solution')
print()
print('To solve the puzzle, you must first travel from world state ', end = '')
for state in range(len(p)-1):
    print(p[state], ' to ', end = ' ')
print(p[-1])
print('Runtime for DFS: ', end-start)
print()