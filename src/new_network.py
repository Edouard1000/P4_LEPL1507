import os
import sys
from parse import parse_airport_data
import utility_functions as uf
import networkx as nx
import pandas as pd
import airpots_plot as ap 
import genetics as gen
import random
import matplotlib.pyplot as plt

def new_network(airport_csv, pre_existing_routes_csv, wanted_journeys_csv, C, WithFinalHillClimb = False, random_seed = 42, make_plot = False, population_size = 1000, generations = 200, mutation_rate = 0.1, print_final_result = False, minutes = 60):

    """
    Fonction principale pour tester l'algorithme de recherche de trajectoire optimale.
    """
    airports_file = airport_csv
    routes_file = pre_existing_routes_csv

    # Dossier de sortie
    output_folder = "./output_csv"
    os.makedirs(output_folder, exist_ok=True)

    
    network_graph, id_to_index = parse_airport_data(airports_file, routes_file)
    network_graph_adj_list = nx.to_dict_of_lists(network_graph)

    index_to_id = {v: k for k, v in id_to_index.items()}
    # print(index_to_id)

    network_graph_adj_matrix = nx.adjacency_matrix(network_graph, weight= "distance").todense()
    df = pd.DataFrame(network_graph_adj_matrix)
    df.to_csv("./output_csv/network_graph_adj_matrix.csv", index=False, header=False)

    
    weights = nx.get_edge_attributes(network_graph, 'distance')
    P = []
    for key in weights.keys():
        P.append((key[0], key[1], weights[key]))
    
    random.seed(random_seed)  # For reproducibility

    J = []
    wanted_journeys = pd.read_csv(wanted_journeys_csv)
    for i in range(len(wanted_journeys)):
        airport1, airport2 = wanted_journeys.iloc[i]
        J.append((airport1, airport2))
    # print(J)

    J = [(id_to_index[t[0]], id_to_index[t[1]]) for t in J]

    optimal_trajectory, evolution = gen.genetic_algorithm(P, J, C, population_size = population_size, generations = generations, mutation_rate = mutation_rate, withFinalHillClimb= WithFinalHillClimb )

    if(make_plot):
        plt.plot(evolution)
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.title('Evolution of Fitness over Generations')
        plt.show()


    # Affichage des résultats
    # print("\n--- Résultat de l'algorithme ---")
    # print("Trajectoire optimale:", optimal_trajectory)

    # Enregistrer la trajectoire optimale dans un fichier CSV
    with open(f"{output_folder}/optimal_trajectory.csv", "w") as file:
        file.write("ID_start,ID_end\n")
        for edge in optimal_trajectory:
            file.write(f"{index_to_id[edge[0]]},{index_to_id[edge[1]]}\n")

    # Vérifier le contenu du fichier de sortie
    with open(f"{output_folder}/optimal_trajectory.csv", "r") as file:
        saved_trajectory = file.read()
        # print("Trajectoire optimale enregistrée dans le fichier:", saved_trajectory)
    # print("here")
    ap.plot_airport_network('csv/airports.csv', 'output_csv/optimal_trajectory.csv', title="New Airport Network")

    # print("evolution = ")
    # print(evolution[len(evolution)-1])

    obt = []
    for edge in optimal_trajectory:
        obt.append((index_to_id[edge[0]], index_to_id[edge[1]]))
    # print("obt = ")
    # print(obt)

    if(print_final_result):
        print("Trajectoire optimale:", obt)
        print("Fitness = ", evolution[len(evolution)-1])    

    return obt, evolution[len(evolution)-1]



new_network("./csv/custom_airports.csv", "./csv/custom_routes.csv", "./csv/custom_J.csv", 1000, True, 42, True, 200, 1000, 0.1, True, 20)
    
