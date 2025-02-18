import sys
import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import copy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from code import dijkstra as dij
import time

def generate_graph(num_nodes=10, prob_edge=0.1, num_starts=5, num_ends_per_start=5):
    graph = nx.DiGraph()
    
    for i in range(num_nodes):
        graph.add_node(i, index = i, latitude = random.uniform(-90, 90), longitude = random.uniform(-180, 180))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < prob_edge:  # 10% de chances d'ajouter une arête
                graph.add_edge(i, j, distance=random.randint(1, 20))  # Poids aléatoire entre 1 et 20

    def generate_paths(graph, num_starts=num_starts, num_ends_per_start=num_ends_per_start):
        nodes = list(graph.nodes)
        starts = random.sample(nodes, num_starts)  # Sélectionne des nœuds de départ aléatoires
        ends = []

        for start in starts:
            possible_ends = [node for node in nodes if node != start]  # Exclut le départ lui-même
            end_nodes = random.sample(possible_ends, min(num_ends_per_start, len(possible_ends)))  # Sélectionne les destinations
            ends.append(end_nodes)

        return starts, ends
    
    starts, endss = generate_paths(graph)
    return graph, starts, endss

def dijkstra_tests(num_nodes=10, prob_edge=0.1, num_starts=5, num_ends_per_start=5):
    graph, starts, endss = generate_graph(num_nodes=num_nodes, prob_edge=prob_edge, num_starts=num_starts, num_ends_per_start=num_ends_per_start)

    start_time = time.time()
    distances, paths = dij.dijkstra_all_paths(graph, starts, copy.deepcopy(endss))
    end_time = time.time()

    start_time3 = time.time()
    distances3, paths3 = dij.optimized_dijkstra(graph, starts, copy.deepcopy(endss))
    end_time3 = time.time()

    start_time4 = time.time()
    distances4, paths4 = dij.dijkstra_adj(nx.to_numpy_array(graph, weight="distance"), starts, copy.deepcopy(endss))
    end_time4 = time.time()

    print(f"Time taken for our Dijkstra's algorithm: {end_time - start_time} seconds")
    print(f"Time taken for optimized Dijkstra's algorithm: {end_time3 - start_time3} seconds")
    print(f"Time taken for adjacency matrix Dijkstra's algorithm: {end_time4 - start_time4} seconds")
    print("our Dijkstra's algorithm is {} times faster than optimized Dijkstra's".format((end_time3 - start_time3)/(end_time - start_time)))
    return distances, distances4, starts, endss, paths, paths4, graph

#------#
#-TEST-#
#------#

distances, distances4, starts, endss, paths, paths4, graph = dijkstra_tests(num_nodes=70, prob_edge=0.5, num_starts=5, num_ends_per_start=5)
print( "VERIF DES DISTANCES ")
for i in range(len(starts)): 
    start = starts[i]  
    for j in endss[i]:
        assert distances[start][j] == distances4[start][j], f"Erreur: {distances[start][j]} != {distances4[start][0][j]}"
        if paths[start][j] != [] and paths[start][j] != None:
            print("Distance entre",start," et ",j," : ",distances[start][j])
            print("Chemin : ",paths[start][j])
            print("CHemin 4 : ",paths4[start][j])
            pass
#pos = nx.spring_layout(graph)  # Positionne les nœuds pour une visualisation claire
#nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=200, font_size=5)
#labels = nx.get_edge_attributes(graph, 'distance')
#nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_size=5)
#plt.show()