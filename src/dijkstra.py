import math
import pandas as pd
import networkx as nx
import math
import heapq
import copy

# ----------------------------
# --- Dijkstra avec Graphe ---
# ----------------------------

"""
Compute the shortest paths from multiple start nodes to multiple end nodes in a graph using Dijkstra's algorithm.
Parameters:
graph (networkx.Graph): The input graph where nodes are indexed and edges have a 'distance' attribute.
starts (list of int): List of starting node indices.
endss (list of list of int): List of lists, where each sublist contains end node indices corresponding to each start node.
Returns:
list of list of float: A 2D list where the element at [i][j] represents the shortest distance from node i to node j.
"""
pass
"""
Compute the shortest paths between all pairs of nodes in a graph using Dijkstra's algorithm.
Parameters:
graph (networkx.Graph): The input graph where nodes are indexed and edges have a 'distance' attribute.
Returns:
dict: A dictionary where keys are source nodes and values are dictionaries with target nodes as keys and shortest path lengths as values.
"""
pass
def dijkstra_all_paths(graph, starts, endss):
    n = len(graph.nodes)
    distances = {}
    paths = {}
    for start in starts:
        ends = set(endss[start])

        distances[start] = [float('inf')] * n
        paths[start] = [None] * n
        distances[start][start] = 0

        priority_queue = [(0, start)]
        visited = [False] * n
        while priority_queue and ends:
            current_distance, current_node = heapq.heappop(priority_queue)
            # No existing road to all the destinations destination
            if current_node is None:
                break
            # If the node has already been visited, skip it
            if visited[current_node]:
                continue
            # If the node is a destination, remove it from the list of destinations
            if current_node in ends:
                ends.remove(current_node)
            visited[current_node] = True
            # For each neighbor of the current node, update the distances and paths
            for neighbor in graph.neighbors(current_node):
                j = graph.nodes[neighbor]["index"]
                new_distance = graph[current_node][neighbor].get("distance", float('inf'))
                if new_distance > 0 and not visited[j]:
                    distance = current_distance + new_distance
                    if distance < distances[start][j]:
                        distances[start][j] = distance
                        if current_node == start:
                            paths[start][j] = []
                        else:
                            paths[start][j] = (paths[start][current_node] or []) + [current_node]
                        heapq.heappush(priority_queue, (distance, j))
    return distances, paths

def optimized_dijkstra(graph, starts, endss):
    distances = {}  
    paths = {}      
    
    for i, start in enumerate(starts):
        ends = set(endss[i])  # Convert to set for fast lookup
        distances[start] = {}
        paths[start] = {}

        # Run NetworkX's optimized Dijkstra for a single source
        shortest_distances, shortest_paths = nx.single_source_dijkstra(graph, start, weight="distance")

        # Store only the necessary results
        for end in ends:
            if end in shortest_distances:  # Avoid KeyError if no path exists
                distances[start][end] = shortest_distances[end]
                paths[start][end] = shortest_paths[end]

    return distances, paths

dist_matrix  = pd.read_csv('./output_csv/network_graph_adj_matrix.csv', header=None).values
def dijkstra_adj_list(adj_list, starts, endss): 
    n = len(dist_matrix) # Number of nodes
    distances = [None] * n # Initialize the distance matrix
    paths = [None] * n # Initialize the path matrix
    for start in starts: # For each start node
        ends = set(endss[start]) # Convert endss of start to set for fast lookup
        distances[start] = [float('inf')] * n # Initialize the distance list for the start node
        paths[start] = [None] * n # Initialize the path list for the start node
        distances[start][start] = 0 # Set the distance from the start node to itself to 0
        priority_queue = [(0, start)] # Initialize the priority queue with the start node
        visited = [False] * n # Initialize the visited list
        while priority_queue and ends: # While the priority queue is not empty and there are still end nodes
            current_distance, current_node = heapq.heappop(priority_queue) # Pop the node with the smallest distance from the priority queue
            if current_node is None: # If the node is None, break
                break
            if visited[current_node] or current_node not in adj_list: # If the node has already been visited or is not in the adjacency list, skip it
                continue
            if current_node in ends: # If the node is an end node, remove it from the list of end nodes
                ends.remove(current_node)
            visited[current_node] = True # Mark the node as visited
            for neighbor in adj_list[current_node]: # For each neighbor of the current node
                new_distance = dist_matrix[current_node][neighbor] # Get the distance from the current node to the neighbor
                if new_distance > 0 and not visited[neighbor]: # If the distance is positive and the neighbor has not been visited
                    distance = current_distance + new_distance # Calculate the new distance
                    if distance < distances[start][neighbor]: # If the new distance is smaller than the current distance
                        distances[start][neighbor] = distance # Update the distance
                        if current_node == start: # If the current node is the start node
                            paths[start][neighbor] = [] # Initialize the path
                        else: # If the current node is not the start node
                            paths[start][neighbor] = (paths[start][current_node] or []) + [current_node] # Update the path
                        heapq.heappush(priority_queue, (distance, neighbor)) # Push the neighbor to the priority queue
    return distances, paths # Return the distance and path matrices

def new_dijkstra_adj_list(adj_list, starts, endss, prev_distances=None, prev_paths=None): 
    n = len(dist_matrix)  # Nombre de nœuds
    distances = prev_distances if prev_distances else [None] * n  # Réutilisation des distances
    paths = prev_paths if prev_paths else [None] * n  # Réutilisation des chemins

    for start in starts:
        if distances[start] is None:  # Si non calculé avant, initialiser
            distances[start] = [float('inf')] * n
            paths[start] = [None] * n
            distances[start][start] = 0

        priority_queue = [(0, start)]
        visited = [False] * n
        ends = set(endss[start])  # Convertir en set pour accès rapide

        while priority_queue and ends:
            current_distance, current_node = heapq.heappop(priority_queue)

            if visited[current_node] or current_node not in adj_list:
                continue

            if current_node in ends:
                ends.remove(current_node)  # Supprimer si atteint

            visited[current_node] = True

            for neighbor in adj_list[current_node]:
                new_distance = dist_matrix[current_node][neighbor]

                if new_distance > 0 and not visited[neighbor]:
                    distance = current_distance + new_distance

                    if distance < distances[start][neighbor]:  # Mise à jour si meilleur chemin trouvé
                        distances[start][neighbor] = distance
                        paths[start][neighbor] = (paths[start][current_node] or []) + [current_node]
                        heapq.heappush(priority_queue, (distance, neighbor))

    return distances, paths  # Retourne les valeurs mises à jour

'''
def new_dijkstra_adj(adjacency, starts, endss, distances, paths, removed_edge):
    u, v = removed_edge  # Arête supprimée
    n = len(adjacency)
    affected_starts = set()

    # Identifier les trajets impactés
    for start in starts:
        for end in endss[starts.index(start)]:
            if paths[start][end] and u in paths[start][end] and v in paths[start][end]:
                affected_starts.add(start)

    # Recalculer Dijkstra uniquement pour les trajets affectés
    for start in affected_starts:
        ends = set(endss[starts.index(start)])
        distances[start] = [float('inf')] * n
        paths[start] = [None] * n
        distances[start][start] = 0
        priority_queue = [(0, start)]
        visited = [False] * n
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if visited[current_node]:
                continue
            visited[current_node] = True
            if current_node in ends:
                ends.remove(current_node)
            for neighbor, new_distance in enumerate(adjacency[current_node]):
                if new_distance > 0 and not visited[neighbor]:
                    distance = current_distance + new_distance
                    if distance < distances[start][neighbor]:
                        distances[start][neighbor] = distance
                        paths[start][neighbor] = (paths[start][current_node] or []) + [current_node]
                        heapq.heappush(priority_queue, (distance, neighbor))

    return distances, paths
'''

