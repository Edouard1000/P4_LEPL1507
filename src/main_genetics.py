import os
import sys
from parse import parse_airport_data
import f as f
import utility_functions as uf
import networkx as nx
import pandas as pd
import airpots_plot as ap 
import genetics as gen

def main():
    """
    Fonction principale pour tester l'algorithme de recherche de trajectoire optimale.
    """
    airports_file = "./csv/airports.csv"
    routes_file = "./csv/pre_existing_routes.csv"

    # Dossier de sortie
    output_folder = "./output_csv"
    os.makedirs(output_folder, exist_ok=True)

    
    network_graph, id_to_index = parse_airport_data(airports_file, routes_file)
    network_graph_adj_list = nx.to_dict_of_lists(network_graph)

    index_to_id = {v: k for k, v in id_to_index.items()}
    print(index_to_id)


    #print(network_graph_adj_list)
    network_graph_adj_matrix = nx.adjacency_matrix(network_graph, weight= "distance").todense()
    df = pd.DataFrame(network_graph_adj_matrix)
    df.to_csv("./output_csv/network_graph_adj_matrix.csv", index=False, header=False)

    
    C = 1

    # Exécuter la recherche de la meilleure trajectoire
    #optimal_trajectory = f.findOptimalTrajectory(network_graph_adj_list, C, output_folder, airport_to_connect_list)
    #P = list(network_graph.edges)
    
    weights = nx.get_edge_attributes(network_graph, 'distance')
    P = []
    for key in weights.keys():
        P.append((key[0], key[1], weights[key]))



    
    temp = [('AMS', 'FRA'), ('TUN','SVO'), ('LOS', 'DMK'), ('BSB', 'LOS')]
    J = [(id_to_index[t[0]], id_to_index[t[1]]) for t in temp]
    print(J)

    optimal_trajectory = gen.genetic_algorithm(P, J, C)

    # Affichage des résultats
    print("\n--- Résultat de l'algorithme ---")
    print("Trajectoire optimale:", optimal_trajectory)

    # Enregistrer la trajectoire optimale dans un fichier CSV
    with open(f"{output_folder}/optimal_trajectory.csv", "w") as file:
        file.write("ID_start,ID_end\n")
        for edge in optimal_trajectory:
            file.write(f"{index_to_id[edge[0]]},{index_to_id[edge[1]]}\n")

    # Vérifier le contenu du fichier de sortie
    with open(f"{output_folder}/optimal_trajectory.csv", "r") as file:
        saved_trajectory = file.read()
        print("Trajectoire optimale enregistrée dans le fichier:", saved_trajectory)
    print("here")
    ap.plot_airport_network('csv/airports.csv', 'output_csv/optimal_trajectory.csv', title="New Airport Network")
if __name__ == "__main__":
    main()
    
