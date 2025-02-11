import math
import pandas as pd
import networkx as nx
import math
import heapq
import copy

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
    distances = [None] * n
    paths = [None] * n
    for i, start in enumerate(starts):
        ends = set(endss[i])
        distances[start] = [float('inf')] * n
        paths[start] = [None] * n
        distances[start][start] = 0
        priority_queue = [(0, start)]
        visited = [False] * n
        while priority_queue and ends:
            current_distance, current_node = heapq.heappop(priority_queue)
            if visited[current_node]:
                continue
            if current_node in ends:
                ends.remove(current_node)
            visited[current_node] = True
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

def dijkstra_all_paths_2(graph):
    return dict(nx.all_pairs_dijkstra(graph, weight="distance"))

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

