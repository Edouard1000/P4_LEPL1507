import math
import pandas as pd
import networkx as nx
import math
import heapq

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
    distances = [[float('inf')] * n for _ in range(n)]
    for i in range(len(starts)):
        start = starts[i]
        ends = endss[i]
        distances[start][start] = 0
        priority_queue = [(0, start)]
        visited = [False] * n
        while priority_queue and ends:
            current_distance, current_node = heapq.heappop(priority_queue)

            if visited[current_node]:
                continue
            else :
                if current_node in ends:
                    ends.remove(current_node)   
            visited[current_node] = True
            for neighbor, weight in graph[current_node].items():
                i = graph.nodes[neighbor]["index"]
                new_distance = weight.get("distance")  
                if new_distance>0 and not visited[i]:
                    # update the distance from current to neighbor if a shorter path is found
                    if distances[current_node][i] < new_distance:
                        distances[current_node][i] = new_distance
                    distance = current_distance + new_distance
                    # update the distance from start to neighbor if a shorter path is found
                    if distance < distances[start][i]:
                        distances[start][i] = distance
                        heapq.heappush(priority_queue, (distance, i))

    return distances

def dijkstra_all_paths_2(graph):
    return dict(nx.all_pairs_dijkstra(graph, weight="distance"))



