import pandas as pd
import networkx as nx
import heapq

import pandas as pd
import networkx as nx
import utility_functions as uf  

def parse_cost(airports_file="./csv/airports.csv", routes_file="./secondary_csv/pre_existing_routes_costs.csv"):
    """
    Parse les fichiers CSV des aéroports et des routes pour construire un graphe dirigé avec indexation des sommets.

    Args:
        airports_file (str): Chemin vers le fichier airports.csv
        routes_file (str): Chemin vers le fichier pre_existing_routes.csv

    Returns:
        dict: Liste d'adjacence avec les indices des sommets
    """
    # Charger les fichiers CSV
    airports_df = pd.read_csv(airports_file)
    routes_df = pd.read_csv(routes_file)

    # Création d'un graphe dirigé
    G = nx.DiGraph()

    # Création d'un mapping ID -> Index
    id_to_index = {}

    # Ajouter les aéroports comme nœuds avec leurs indices
    for i, (_, row) in enumerate(airports_df.iterrows()):
        airport_id = row["ID"]
        id_to_index[airport_id] = i  # Associer l'ID à un index unique
        G.add_node(i,  # Utilisation de `i` comme index
                   name=row["name"], 
                   city=row["city"], 
                   country=row["country"], 
                   latitude=row["latitude"], 
                   longitude=row["longitude"],
                   ID = airport_id)

    # Ajouter les routes existantes comme arêtes
    for _, row in routes_df.iterrows():
        start_id, end_id, cost = row["ID_start"], row["ID_end"], row["cost"]
        if start_id in id_to_index and end_id in id_to_index:
            start_idx, end_idx = id_to_index[start_id], id_to_index[end_id]
            G.add_edge(start_idx, end_idx, distance=cost)

    return G, id_to_index

def dijkstra_time(adj_list, starts, endss, stopover, time_matrix):
    n = len(time_matrix)
    times = [None] * n
    paths = [None] * n
    for start in starts:
        ends = set(endss[start])
        times[start] = [float('inf')] * n
        paths[start] = [None] * n
        times[start][start] = 0
        priority_queue = [(0, start)]
        visited = [False] * n
        while priority_queue and ends:
            current_time, current_node = heapq.heappop(priority_queue)
            if current_node is None:
                break
            if visited[current_node] or current_node not in adj_list:
                continue
            if current_node in ends:
                ends.remove(current_node)
            visited[current_node] = True
            for neighbor in adj_list[current_node]:
                new_time = dist_to_time(time_matrix[current_node][neighbor])
                if new_time > 0 and not visited[neighbor]:
                    additional_time = stopover if current_node != start else 0
                    time = current_time + new_time + additional_time
                    if time < times[start][neighbor]:
                        times[start][neighbor] = time
                        if current_node == start:
                            paths[start][neighbor] = []
                        else:
                            paths[start][neighbor] = (paths[start][current_node] or []) + [current_node]
                        heapq.heappush(priority_queue, (time, neighbor))
    return times, paths

def dist_to_time(distance_km, cruise_speed_kmh=900, extra_time=0.75):
    """
    Convert flight distance to estimated travel time.

    Parameters:
    - distance_km (float): Distance between two airports in kilometers.
    - cruise_speed_kmh (float): Speed of the aircraft in km/h (default 900 km/h).
    - extra_time (float): Additional time for takeoff and landing in hours (default 45 min -> 0.75 h).

    Returns:
    - float: Estimated flight duration in hours.
    """
    if distance_km <= 0:
        return 0  # No travel if distance is zero or invalid

    cruise_time = distance_km / cruise_speed_kmh  # Time spent cruising
    total_time = cruise_time + extra_time  # Adding takeoff & landing time
    return total_time


cost_graph, id_to_index2 = parse_cost()
network_graph_adj_matrix_price = nx.adjacency_matrix(cost_graph, weight= "distance").todense()
df_price = pd.DataFrame(network_graph_adj_matrix_price)
df_price.to_csv("./output_csv/network_graph_adj_matrix_costs.csv", index=False)