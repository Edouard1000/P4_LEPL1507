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
    id_to_index = {}
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
    warning = True
    for _, row in routes_df.iterrows():
        try :
            start_id, end_id = row["ID_start"], row["ID_end"]
            if start_id in id_to_index and end_id in id_to_index:
                start_idx, end_idx = id_to_index[start_id], id_to_index[end_id]
                x = (G.nodes[start_idx]["latitude"], G.nodes[start_idx]["longitude"])
                y = (G.nodes[end_idx]["latitude"], G.nodes[end_idx]["longitude"])
                G.add_edge(start_idx, end_idx, distance=uf.earth_distance(*x, *y))
        except Exception :
            if warning == True:
                print("carefull one preexisting route is ignore because not in airport ! ")
                Warning = False


    return G, id_to_index

def parse_cost(airports_file="./csv/airports.csv", routes_file="./csv/pre_existing_routes.csv"):
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
    costs_df = pd.read_csv("./csv/prices.csv")

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
        cost = costs_df.loc[costs_df['ID_start'] == row["ID_start"]].loc[costs_df['ID_end'] == row["ID_end"]].iloc[0]["price_tag"]
        start_id, end_id = row["ID_start"], row["ID_end"]
        if start_id in id_to_index and end_id in id_to_index:
            start_idx, end_idx = id_to_index[start_id], id_to_index[end_id]
            G.add_edge(start_idx, end_idx, distance=cost)

    return G, id_to_index

def parse_flow_network(
    airports_file="./csv/airports.csv",
    routes_file="./csv/pre_existing_routes.csv",
    airport_caps_file="./csv/capacities_airports.csv",
    connection_caps_file="./csv/capacities_connexions.csv"
):
    """
    Construit un graphe dirigé avec :
    - les aéroports comme sommets (avec capacité),
    - les routes comme arêtes (avec capacité et distance),
    - les distances comme poids d’arêtes (optimisation).

    Returns:
        G (nx.DiGraph): Graphe dirigé avec attributs.
        id_to_index (dict): Mapping des ID d’aéroports vers leur index interne.
    """

    # Chargement des fichiers CSV
    airports_df = pd.read_csv(airports_file)
    routes_df = pd.read_csv(routes_file).rename(columns={"ID_start": "from", "ID_end": "to"})
    airport_caps_df = pd.read_csv(airport_caps_file)
    conn_caps_df = pd.read_csv(connection_caps_file).rename(columns={
        "ID_start": "from",
        "ID_end": "to",
        "connexion capacity": "capacity" 
    })

    # Suppression de colonnes parasites éventuelles
    if "Unnamed: 0" in conn_caps_df.columns:
        conn_caps_df.drop(columns=["Unnamed: 0"], inplace=True)

    # Initialisation du graphe
    G = nx.DiGraph()
    global id_to_index
    id_to_index = {}

    # Ajout des aéroports (nœuds)
    for i, (_, row) in enumerate(airports_df.iterrows()):
        airport_id = row["ID"]
        id_to_index[airport_id] = i
        G.add_node(i,
                   name=row.get("name", ""),
                   city=row.get("city", ""),
                   country=row.get("country", ""),
                   latitude=row["latitude"],
                   longitude=row["longitude"],
                   ID=airport_id,
                   capacity=None)

    # Ajout des capacités des aéroports (nœuds)
    for _, row in airport_caps_df.iterrows():
        airport_code = row["airportsID"]
        if airport_code in id_to_index:
            idx = id_to_index[airport_code]
            G.nodes[idx]["capacity"] = row["capacity"]

    # Ajout des arêtes avec capacité et distance
    routes_df = routes_df.merge(conn_caps_df, on=["from", "to"])
    for _, row in routes_df.iterrows():
        start_id, end_id = row["from"], row["to"]
        if start_id in id_to_index and end_id in id_to_index:
            u, v = id_to_index[start_id], id_to_index[end_id]
            x = (G.nodes[u]["latitude"], G.nodes[u]["longitude"])
            y = (G.nodes[v]["latitude"], G.nodes[v]["longitude"])
            distance = uf.earth_distance(*x, *y)
            G.add_edge(u, v,
                       capacity=row["capacity"],
                       distance=distance,
                       weight=distance)

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
