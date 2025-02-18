import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code")))

import f  # Pas besoin de "as f"
import parse
import airpots_plot as ap

network_graph_test = parse.parse_airport_data(airports_file = "./csv/testFileAirports.csv", routes_file = "./csv/testFilePreExistingRoutes.csv")  
output_folder = "output¨csv"
f.findOptimalTrajectory(network_graph_test,C , output_folder, Airport_to_connect_list)

ap.plot_airport_network('csv/airports.csv', output_folder, title="Global Airport Network")

size = os.path.getsize(output_folder)

print("taille du nouveau network" + str(size))