import os
import sys
<<<<<<< HEAD:python_files/main.py
from parse import parse_airport_data
import f as f
import utility_functions as uf
=======
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './python_files')))
from src.parse import parse_airport_data
import src.f as f
import src.utility_functions as uf
>>>>>>> 49e3f45d220135a3858a6aec4934c7aba03826a0:src/main.py
import networkx as nx
import pandas as pd

def main():
    """
    Fonction principale pour tester l'algorithme de recherche de trajectoire optimale.
    """
    airports_file = "./csv/airports.csv"
    routes_file = "./csv/pre_existing_routes.csv"

    
    network_graph = parse_airport_data(airports_file, routes_file)
    network_graph_adj_list = nx.to_dict_of_lists(network_graph)
    # print(network_graph_adj_list)
    network_graph_adj_matrix = nx.adjacency_matrix(network_graph, weight= "distance").todense()
    df = pd.DataFrame(network_graph_adj_matrix)
    df.to_csv("output_csv/network_graph_adj_matrix.csv", index=False)
    airport_to_connect_list = [[0,1]] # à completer

    
    C = 5

    # Dossier de sortie
    output_folder = "output_csv"
    os.makedirs(output_folder, exist_ok=True)

    # Exécuter la recherche de la meilleure trajectoire
    optimal_trajectory = f.findOptimalTrajectory(network_graph_adj_list, C, output_folder, airport_to_connect_list)

    # Affichage des résultats
    print("\n--- Résultat de l'algorithme ---")
    print("Trajectoire optimale:", optimal_trajectory)

    # Vérifier le contenu du fichier de sortie
    with open(f"{output_folder}/optimal_trajectory.txt", "r") as file:
        saved_trajectory = file.read()
        print("Trajectoire optimale enregistrée dans le fichier:", saved_trajectory)

if __name__ == "__main__":
    main()
