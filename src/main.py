import os
from parse import parse_airport_data, parse_cost
from graphic_interface import graphic_interface
import random
import genetics as gen
import matplotlib.pyplot as plt
import pandas as pd
import threading
import webbrowser
import networkx as nx
import pandas as pd
import airpots_plot as ap 

def main():
    """
    Fonction principale pour tester l'algorithme de recherche de trajectoire optimale.
    """

    # Dossiers en entrée
    airports_file = "./csv/airports.csv"
    routes_file = "./csv/pre_existing_routes.csv"
    wanted_journeys_csv = "./csv/wanted_journeys.csv"
    costs_file = "./csv/costs.csv"
    wainting_times_file = "./csv/waiting_times.csv"


    # Dossier de sortie
    output_folder = "./output_csv"
    os.makedirs(output_folder, exist_ok=True)
    adj_matrix = "./output_csv/network_graph_adj_matrix.csv"
    adj_matrix_costs = "./output_csv/network_graph_adj_matrix_costs.csv"

    # --------------------
    # ------- Parse ------
    # --------------------
    print("----------- START PARSING --------------\n ")
    airports = pd.read_csv(airports_file)
    print("Parsing Distances ...")
    network_graph, id_to_index = parse_airport_data(airports_file, routes_file)
    print("Parsing costs ...")
    cost_graph, _ = parse_cost()   

    index_to_id = {v: k for k, v in id_to_index.items()}

    network_graph_adj_matrix = nx.adjacency_matrix(network_graph, weight= "distance").todense()
    df = pd.DataFrame(network_graph_adj_matrix)
    df.to_csv(adj_matrix, index=False, header=False)

    network_graph_adj_matrix_price = nx.adjacency_matrix(cost_graph, weight= "distance").todense()
    df_price = pd.DataFrame(network_graph_adj_matrix_price)
    df_price.to_csv(adj_matrix_costs, index=False, header=False)

    print("Parsing Time ...\n")
    waiting_time = pd.read_csv("./csv/waiting_times.csv", header=None).values
    waiting_time = pd.DataFrame(waiting_time)
    waiting_time.columns = waiting_time.iloc[0]  # Set the first row as the header
    waiting_time = waiting_time.drop(0).reset_index(drop=True)
    waiting_time['idle_time'] = waiting_time['idle_time'].astype(float)

    # ------------------------
    # -- Genetic Algorithm ---
    # ------------------------
    print("----------- GENETICS ALGORITHM --------------\n \n")
    C = 1000
    optimal_trajectory, evolution = compute_genetics(C, random_seed = 42, population_size = 1000, generations = 200, mutation_rate = 0.2, network_graph = network_graph, id_to_index = id_to_index, wanted_journeys_csv = wanted_journeys_csv)
    if(True):
        plt.plot(evolution)
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.title('Evolution of Fitness over Generations')
        plt.show()
#
    ## ------------------------
    ## --- Plot the network ----
    ## ------------------------
#
    print("\n--- Résultat de l'algorithme ---")
    print("Trajectoire optimale:", optimal_trajectory)

    # Enregistrer la trajectoire optimale dans un fichier CSV
    with open("output_csv/optimal_trajectory.csv", "w") as file:
        file.write("ID_start,ID_end\n")
        for edge in optimal_trajectory:
            file.write(f"{index_to_id[edge[0]]},{index_to_id[edge[1]]}\n")
    # Vérifier le contenu du fichier de sortie
    with open(f"{output_folder}/optimal_trajectory.csv", "r") as file:
        saved_trajectory = file.read()
    ap.plot_airport_network(airports_file, 'output_csv/optimal_trajectory.csv', title="New Airport Network")

    obt = []
    for edge in optimal_trajectory:
        obt.append((index_to_id[edge[0]], index_to_id[edge[1]]))

    if(True):
        print("Trajectoire optimale:", obt)
        print("Fitness = ", evolution[len(evolution)-1])  
    
    # --------------------------
    # --- Graphic Interface ----
    # --------------------------
    print("----------- LAUNCHING THE INTERFACE --------------\n")

    # exécute l'interface graphique à partir du graphe original
    # app = graphic_interface(airports, cost_graph, network_graph, waiting_time, network_graph_adj_matrix_price, network_graph_adj_matrix)

    # exécute l'interface graphique à partir du graphe modifié

    print("--- Press CTRL+C to stop the server")
    print("--- Press CTRL+Click on the IP address to open the interface in a new tab\n")
    network_graph2, id_to_index = parse_airport_data(routes_file='output_csv/optimal_trajectory.csv')
    cost_graph, _ = parse_cost(routes_file='output_csv/optimal_trajectory.csv')
    network_graph_adj_matrix2 = nx.adjacency_matrix(network_graph, weight= "distance").todense()
    df = pd.DataFrame(network_graph_adj_matrix)
    df.to_csv("./output_csv/optimal_network_graph_adj_matrix.csv", index=False, header=False)

    network_graph_adj_matrix_price2 = nx.adjacency_matrix(cost_graph, weight= "distance").todense()
    df_price = pd.DataFrame(network_graph_adj_matrix_price)
    df_price.to_csv("./output_csv/optimal_network_graph_adj_matrix_costs.csv", index=False)

    print(network_graph2.edges(data=True))
    app = graphic_interface(airports, cost_graph, network_graph2, waiting_time, network_graph_adj_matrix_price2, network_graph_adj_matrix2)
    app.run_server(debug=True, use_reloader=False)

    print("----------- PROGRAM EXECUTED SUCCESSFULLY --------------")

    # -----------
    # --- END ---
    # -----------


def compute_genetics(C, random_seed = 42, population_size = 1000, generations = 200, mutation_rate = 0.1, network_graph = None, id_to_index = None, wanted_journeys_csv = None):
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

    return gen.genetic_algorithm(P, J, C, population_size = population_size, generations = generations, mutation_rate = mutation_rate)

    
if __name__ == "__main__":
    main()
    
