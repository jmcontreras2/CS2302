import matplotlib.pyplot as plt
import numpy as np
#import graph_AL as graph
#import graph_AM as graph # Replace line 3 by this one to demonstrate adjacy maxtrix implementation
import graph_EL as graph # Replace line 3 by this one to demonstrate edge list implementation

if __name__ == "__main__":   
    plt.close("all")  
    print('Undirected, Unweighted Graph')
    g = graph.Graph(6)
    g.insert_edge(0,1)
    g.insert_edge(0,2)
    g.insert_edge(1,2)
    g.insert_edge(2,3)
    g.insert_edge(3,4)
    g.insert_edge(4,1)
    print()
    g.display()
    print()
    g.draw()
    a = g.as_AM()
    a.display()
    print()
    
    g.delete_edge(1,2)
    g.display()
    print()
    g.draw()
        
    print('Directed, Unweighted Graph')
    g = graph.Graph(6,directed = True)
    g.insert_edge(0,1)
    g.insert_edge(0,2)
    g.insert_edge(1,2)
    g.insert_edge(2,3)
    g.insert_edge(3,4)
    g.insert_edge(4,1)
    print()
    g.display()
    print()
    g.draw()
    
    a = g.as_AM()
    a.display()
    print()

    g.delete_edge(1,2)
    g.display()
    print()
    g.draw()
    
    print('Undirected, Weighted Graph')
    g = graph.Graph(6,weighted=True)
    g.insert_edge(0,1,4)
    g.insert_edge(0,2,3)
    g.insert_edge(1,2,2)
    g.insert_edge(2,3,1)
    g.insert_edge(3,4,5)
    g.insert_edge(4,1,4)
    print()
    g.display()
    print()
    g.draw()    
    
    a = g.as_AM()
    a.display()
    print()
    
    
    g.delete_edge(1,2)
    print()
    g.display()
    print()
    g.draw()
    
    print('Directed, Weighted Graph')
    g = graph.Graph(6,weighted=True,directed = True)
    g.insert_edge(0,1,4)
    g.insert_edge(0,2,3)
    g.insert_edge(1,2,2)
    g.insert_edge(2,3,1)
    g.insert_edge(3,4,5)
    g.insert_edge(4,1,4)
    print()
    g.display()
    print()
    g.draw()

    a = g.as_AM()
    a.display()
    print()
    
    g.delete_edge(1,2)
    print()
    g.display()
    print()
    g.draw()