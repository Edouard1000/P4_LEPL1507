import sys
import os
import random
import networkx as nx
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from code import utility_functions as uf

def dijkstra_tests():
    graph = nx.DiGraph()
    
    for i in range(100):
        graph.add_node(i)

    for i in range(100):
        for j in range(100):
            if i != j and random.random() < 0.1:  # 10% de chances d'ajouter une arête
                graph.add_edge(i, j, weight=random.randint(1, 20))  # Poids aléatoire entre 1 et 20

    return graph