import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './python_files')))
from python_files.parse import parse_airport_data
import python_files.f as f
import python_files.utility_functions




def main():
    """
    Fonction principale pour tester l'algorithme de recherche de trajectoire optimale.
    """
    airports_file = "./csv/airports.csv"
    routes_file = "./csv/pre_existing_routes.csv"

    
    network_graph = parse_airport_data(airports_file, routes_file)

    
    airport_to_connect_list = [[0,1]] # à completer

    
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
