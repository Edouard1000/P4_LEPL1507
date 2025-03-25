import networkx as nx
from scipy.optimize import linprog
import numpy as np
import csv

def read_airports(filename):
    """
    Lit le fichier capacities_airports.csv et retourne un dictionnaire
    avec les identifiants d'aéroport et leur capacité.
    """
    airports = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # On lit l'identifiant et la capacité (en ignorant la première colonne d'index)
            airport_id = row['airportsID']
            capacity = int(row['capacity'])
            airports[airport_id] = capacity
    return airports

def read_connections(filename, default_cost=1):
    """
    Lit le fichier capacities_connexions.csv et retourne une liste de tuples
    (origin, destination, capacity, cost).
    
    Ici, comme il n'y a pas de coût, on assigne default_cost à chaque connexion.
    """
    connections = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            origin = row['ID_start']
            destination = row['ID_end']
            capacity = int(row['connexion capacity'])
            cost = default_cost  # Coût par défaut, à adapter selon vos besoins
            connections.append((origin, destination, capacity, cost))
    return connections


def minimum_time_flow(graph, populations, target):
    """
    Trouve le temps minimum et les arêtes à utiliser pour rassembler toute la population au noeud cible.
    
    :param graph: Graph dirigé (NetworkX DiGraph)
    :param populations: Dictionnaire {noeud: population}
    :param target: Noeud cible où rassembler toute la population
    :return: Dictionnaire indiquant les flux sur chaque arête et le temps total
    """
    
    # Création du modèle d'optimisation linéaire
    edges = list(graph.edges(data=True))
    n_edges = len(edges)
    nodes = list(graph.nodes())
    n_nodes = len(nodes)
    node_index = {node: i for i, node in enumerate(nodes)}
    
    # Matrice des contraintes d'équilibre de flux
    A_eq = np.zeros((n_nodes, n_edges))
    b_eq = np.zeros(n_nodes)
    
    # Vecteurs de coût (temps) et de capacité
    cost = np.zeros(n_edges)
    bounds = []
    
    for j, (u, v, data) in enumerate(edges):
        A_eq[node_index[u], j] = -1  # Sortie du noeud u
        A_eq[node_index[v], j] = 1   # Entrée dans le noeud v
        cost[j] = 0  # On optimise par niveau, donc le coût initial est 0
        bounds.append((0, data['capacity']))  # Capacité de l'arête
    
    # Définir les besoins en flux
    for node, pop in populations.items():
        if node == target:
            b_eq[node_index[node]] = sum(populations.values())  # Réception de toute la population
        else:
            b_eq[node_index[node]] = -pop  # Chaque nœud doit envoyer sa population
    
    # Résolution du problème avec linprog
    result = linprog(cost, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    
    if result.success:
        flow_values = result.x
        flows = {(edges[j][0], edges[j][1]): flow_values[j] for j in range(n_edges) if flow_values[j] > 0}
        
        # Calcul du temps total basé sur le chemin le plus long à chaque étape
        node_times = {target: 0}  # Le nœud cible est atteint en 0 temps
        sorted_nodes = sorted(nodes, key=lambda x: -populations.get(x, 0))  # Traitement par ordre décroissant de population
        
        for node in sorted_nodes:
            if node == target:
                continue
            incoming_edges = [(u, v, data) for u, v, data in edges if v == node and (u, v) in flows]
            if incoming_edges:
                max_time = max(node_times[u] + data['time'] for u, v, data in incoming_edges)
                node_times[node] = max_time
        
        total_time = max(node_times.values())
        return flows, total_time
    else:
        return None, None

# Exemple d'utilisation
graph = nx.DiGraph()
graph.add_edge('Marseille', 'Berlin', capacity=100, time=2)
graph.add_edge('Paris', 'Berlin', capacity=100, time=1)
graph.add_edge('Berlin', 'Moscou', capacity=200, time=2)

populations = {'Marseille': 100, 'Paris': 100, 'Berlin': 0, 'Moscou': 0}
target = 'Moscou'

flows, total_time = minimum_time_flow(graph, populations, target)
print("Flux optimal :", flows)
print("Temps total minimum :", total_time)
