import os
import sys
from parse import parse_airport_data
from secondary_parse import parse_cost
import f as f
import utility_functions as uf
import networkx as nx
import pandas as pd
import airpots_plot as ap 

def main():
    """
    Fonction principale pour tester l'algorithme de recherche de trajectoire optimale.
    """
    airports_file = "./csv/airports_europe.csv"
    routes_file = "./csv/pre_existing_routes_europe.csv"

    # Dossier de sortie
    output_folder = "./output_csv"
    os.makedirs(output_folder, exist_ok=True)

    
    network_graph, id_to_index = parse_airport_data(airports_file, routes_file)
    network_graph_adj_list = nx.to_dict_of_lists(network_graph)


    #print(network_graph_adj_list)
    network_graph_adj_matrix = nx.adjacency_matrix(network_graph, weight= "distance").todense()
    df = pd.DataFrame(network_graph_adj_matrix)
    df.to_csv("./output_csv/network_graph_adj_matrix.csv", index=False)
    airport_to_connect_list = [[7,4]] # à completer

    C = 65

    # Exécuter la recherche de la meilleure trajectoire
    optimal_trajectory = f.findOptimalTrajectory(network_graph_adj_list, C, output_folder, airport_to_connect_list)

    # Affichage des résultats
    print("\n--- Résultat de l'algorithme ---")
    print("Trajectoire optimale:", optimal_trajectory)

    # Vérifier le contenu du fichier de sortie
    with open(f"{output_folder}/optimal_trajectory.csv", "r") as file:
        saved_trajectory = file.read()
        print("Trajectoire optimale enregistrée dans le fichier:", saved_trajectory)
    ap.plot_airport_network('csv/airports_europe.csv', 'output_csv/optimal_trajectory.csv', title="New Airport Network")
if __name__ == "__main__":
    main()
    
