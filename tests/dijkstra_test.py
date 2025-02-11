import sys
import os
import random
import networkx as nx
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from code import utility_functions as uf
from code import dijkstra as dij
import time

def generate_graph():
    graph = nx.DiGraph()
    
    for i in range(20):
        graph.add_node(i, index = i, latitude = random.uniform(-90, 90), longitude = random.uniform(-180, 180))

    for i in range(20):
        for j in range(20):
            if i != j and random.random() < 0.1:  # 10% de chances d'ajouter une arête
                graph.add_edge(i, j, distance=random.randint(1, 20))  # Poids aléatoire entre 1 et 20

    def generate_paths(graph, num_starts=10, num_ends_per_start=5):
        nodes = list(graph.nodes)
        starts = random.sample(nodes, num_starts)  # Sélectionne des nœuds de départ aléatoires
        ends = []

        for start in starts:
            possible_ends = [node for node in nodes if node != start]  # Exclut le départ lui-même
            end_nodes = random.sample(possible_ends, min(num_ends_per_start, len(possible_ends)))  # Sélectionne les destinations
            ends.append(end_nodes)

        return starts, ends
    
    starts, endss = generate_paths(graph, num_starts=len(graph.nodes), num_ends_per_start=len(graph.nodes)//3)
    return graph, starts, endss

def dijkstra_tests():
    graph, starts, endss = generate_graph()

    start_time = time.time()
    distances = dij.dijkstra_all_paths(graph, starts, endss)
    end_time = time.time()
    print(f"Time taken for our Dijkstra's algorithm: {end_time - start_time} seconds")
    start_time = time.time()
    distances2 = dij.dijkstra_all_paths_2(graph)
    end_time = time.time()
    print(f"Time taken for NetworkX's Dijkstra's algorithm: {end_time - start_time} seconds")
    return distances,distances2, graph, starts, endss

distances, distances2, graph, starts, endss = dijkstra_tests()
print( "VERIF DES DISTANCES :")
for i in starts:
    for j in endss[i]:
        if j in distances2[i][0]:
            print(f"Distance entre {i} et {j} : {distances[i][j]}")
            print(f"Distance 2 entre {i} et {j} : {distances2[i][0][j]}")
            assert distances[i][j] == distances2[i][0][j], f"Erreur entre {i} et {j} : {distances[i][j]} != {distances2[i][0][j]}"
import matplotlib.pyplot as plt

pos = nx.spring_layout(graph)  # Positionne les nœuds pour une visualisation claire
nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=200, font_size=5)
labels = nx.get_edge_attributes(graph, 'distance')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
plt.show()