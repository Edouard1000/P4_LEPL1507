import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './code')))
import code.parse as parse
import networkx as nx
import code.utility_functions as uf
import code.dijkstra as dij
import code.f as f




def main():
    """
    Fonction principale pour tester l'algorithme de recherche de trajectoire optimale.
    """
    airports_file = "./csv/airports.csv"
    routes_file = "./csv/pre_existing_routes.csv"

    
    network_graph = parse.parse_airport_data(airports_file, routes_file)

    
    airport_to_connect_list = None # à completer

    
    C = 5

    # Dossier de sortie
    output_folder = "output_csv"
    os.makedirs(output_folder, exist_ok=True)

    # Exécuter la recherche de la meilleure trajectoire
    optimal_trajectory = f.findOptimalTrajectory(network_graph, C, output_folder, airport_to_connect_list)

    # Affichage des résultats
    print("\n--- Résultat de l'algorithme ---")
    print("Trajectoire optimale:", optimal_trajectory)

    # Vérifier le contenu du fichier de sortie
    with open(f"{output_folder}/optimal_trajectory.txt", "r") as file:
        saved_trajectory = file.read()
        print("Trajectoire optimale enregistrée dans le fichier:", saved_trajectory)

if __name__ == "__main__":
    main()
