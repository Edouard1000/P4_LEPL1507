import pandas as pd
import networkx as nx
import utility_functions as uf

def parse_airport_data(airports_file = "./csv/airports.csv", routes_file = "./csv/pre_existing_routes.csv"):
    """
    Parse les fichiers CSV des aéroports et des routes pour construire un graphe dirigé.
    
    Args:
        airports_file (str): Chemin vers le fichier airports.csv
        routes_file (str): Chemin vers le fichier pre_existing_routes.csv
    
    Returns:
        networkx.DiGraph: Graphe dirigé représentant le réseau aérien
    """
    # Charger les fichiers CSV
    airports_df = pd.read_csv(airports_file)
    routes_df = pd.read_csv(routes_file)
    
    # Création d'un graphe dirigé
    G = nx.DiGraph()
    
    # Ajouter les aéroports comme nœuds avec leurs informations
    i=0
    for _, row in airports_df.iterrows():
        G.add_node(row["ID"], 
                   index=i,
                   name=row["name"], 
                   city=row["city"], 
                   country=row["country"], 
                   latitude=row["latitude"], 
                   longitude=row["longitude"])
        i+=1
    
    # Ajouter les routes existantes comme arêtes
    for _, row in routes_df.iterrows():
        if row["ID_start"] in G.nodes and row["ID_end"] in G.nodes:
            x = (G.nodes[row["ID_start"]]["latitude"], G.nodes[row["ID_start"]]["longitude"])
            y = (G.nodes[row["ID_end"]]["latitude"], G.nodes[row["ID_end"]]["longitude"])
            G.add_edge(row["ID_start"], row["ID_end"], distance=uf.earth_distance(*x, *y))
    
    return G

# Exemple d'utilisation
network_graph = parse_airport_data()

# Vérification : nombre de nœuds et d'arêtes
print(f"Nombre d'aéroports: {network_graph.number_of_nodes()}")
print(f"Nombre de routes: {network_graph.number_of_edges()}")
