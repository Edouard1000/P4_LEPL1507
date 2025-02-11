import math
import pandas as pd
import networkx as nx
import math
import heapq

def dijkstra_all_paths(graph, starts, endss):
    n = len(graph.nodes)
    distances = [[float('inf')] * n for _ in range(n)]
    for i in range(len(start)):
        start = starts[i]
        ends = endss[i]
        distances[start] = 0
        priority_queue = [(0, start)]
        visited = [False] * n
        
        while priority_queue & ends:
            current_distance, current_node = heapq.heappop(priority_queue)

            if visited[current_node]:
                continue
            else :
                if current_node in ends:
                    ends.remove(current_node)   
            visited[current_node] = True
            for i, weight in graph[current_node].items():
                if weight.get("distance") > 0 and not visited[i]:
                    distance = current_distance + weight.get("distance")
                    if distance < distances[start][i]:
                        distances[start][i] = distance
                        distances[i][start] = distance
                        heapq.heappush(priority_queue, (distance, i))

    return distances

def dijkstra_all_paths_2(graph):
    return dict(nx.all_pairs_dijkstra(graph, weight="distance"))

