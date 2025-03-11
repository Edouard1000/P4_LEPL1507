import pandas as pd
import networkx as nx

import pandas as pd
import networkx as nx
import utility_functions as uf  

id_to_index = {}

def parse_airport_data(airports_file="./csv/airports.csv", routes_file="./csv/pre_existing_routes.csv"):
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
        start_id, end_id = row["ID_start"], row["ID_end"]
        if start_id in id_to_index and end_id in id_to_index:
            start_idx, end_idx = id_to_index[start_id], id_to_index[end_id]
            x = (G.nodes[start_idx]["latitude"], G.nodes[start_idx]["longitude"])
            y = (G.nodes[end_idx]["latitude"], G.nodes[end_idx]["longitude"])
            G.add_edge(start_idx, end_idx, distance=uf.euclidean_distance(*x, *y))

    return G, id_to_index

def indexToId(index):
    for key in id_to_index:
        if id_to_index[key] == index:
            return key
    return None


# Exemple d'utilisation
# network_graph, id_to_index = parse_airport_data()


# network_graph_test, id_to_index = parse_airport_data(airports_file = "./csv/testFileAirports.csv", routes_file = "./csv/testFilePreExistingRoutes.csv")  

# Vérification : nombre de nœuds et d'arêtes du graphe de test
