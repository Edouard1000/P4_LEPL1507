import os
import sys
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Ajouter le dossier contenant les fichiers Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



# Importer les modules nécessaires
from python_files.parse import parse_airport_data
import python_files.f as f
import python_files.utility_functions
import python_files.airpots_plot as ap 

def testOnSmallSample(airports_file, routes_file, airport_to_connect_list, C=5):
    """
    Fonction principale pour tester l'algorithme et afficher le réseau optimisé.
    """
    # Charger le réseau aérien
    network_graph = parse_airport_data(airports_file, routes_file)

    # Dossier de sortie
    output_folder = "output_csv"

    # Exécuter la recherche de la meilleure trajectoire
    optimal_trajectory = f.findOptimalTrajectory(network_graph, C, output_folder, airport_to_connect_list)

    # Affichage des résultats
    print("\n--- Résultat de l'algorithme ---")
    print("Trajectoire optimale:", optimal_trajectory)

    # Vérifier le contenu du fichier de sortie
    with open(f"{output_folder}/optimal_trajectory.txt", "r") as file:
        saved_trajectory = file.read()
        print("Trajectoire optimale enregistrée dans le fichier:", saved_trajectory)

    # ---- PLOT ----
    
    # Charger les aéroports pour la visualisation
    airports_df = pd.read_csv(airports_file)

    # Charger les routes initiales
    routes_df = pd.read_csv(routes_file)

    # Créer le graphe optimisé en ne gardant que les routes sélectionnées
    optimized_network = nx.DiGraph()
    
    index = 0  # Pour parcourir la liste `optimal_trajectory`
    for _, row in routes_df.iterrows():
        if optimal_trajectory[index] == 1:  # Si la route a été retenue
            optimized_network.add_edge(row['source'], row['destination'])
        index += 1

    # Tracer le réseau optimisé
    print("\n--- Affichage du réseau optimisé ---")
    ap.plot_airport_network(airports_df, optimized_network, title="Réseau Aérien Optimisé")

if __name__ == "__main__":
    # Fichiers CSV à utiliser
    airports_file = "./csv/testFileAirports.csv"
    routes_file = "./csv/testFIlePreExistingRoutes.csv"

    # Liste des trajets à optimiser
    airport_to_connect_list = [[0, 1]]  # Exemple, à modifier selon ton test

    
    testOnSmallSample(airports_file, routes_file, airport_to_connect_list, C=5)
