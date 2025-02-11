import math
import pandas as pd
import networkx as nx
import math
import heapq
from geographiclib.geodesic import Geodesic

geod = Geodesic.WGS84
RAYON_TERRESTRE = 6371.009

# Calcul distance entre deux points GPS
# Pre : x et y sont des listes ou tuples de coordonées gps en degrés (float)
def euclidean_distance(x, y):
    # Conversion des degrés en radians
    lat1 = math.radians(x[0])
    lon1 = math.radians(x[1])
    lat2 = math.radians(y[0])
    lon2 = math.radians(y[1])


    # Phi et Lambda représentent respectivement la latitude et la longitude en radians
    delta_phi = lat2 - lat1
    delta_lambda = lon2 - lon1

    # Calcul de la distance avec la formule de Haversine
    c = (math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2))
    d = 2 * math.atan2(math.sqrt(c), math.sqrt(1-c))
    return RAYON_TERRESTRE * d

def shortest_path(graph, start_node, end_node):
    return nx.dijkstra_path(graph, start_node, end_node, weight="distance")

def dijkstra(adjacence_matrix, start, end): # arêter Dijkstra dès qu'on atteint le noeud de fin? | modifier le poids des arêtes : poids_i,j = poids_i,j + C
    n = len(adjacence_matrix)
    distances = [float('inf')] * n
    distances[start] = 0
    priority_queue = [(0, start)]
    visited = [False] * n

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if visited[current_node]:
            continue

        visited[current_node] = True

        for neighbor, weight in enumerate(adjacence_matrix[current_node]):
            if weight > 0 and not visited[neighbor]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances[end]



def earth_distance(lat1, lon1, lat2, lon2):
    g = geod.Inverse(lat1, lon1, lat2, lon2)
    return g['s12'] / 1000  # Conversion de la distance en kilomètres

